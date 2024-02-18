package com.example.optimusspectrum

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import kotlinx.serialization.Serializable
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json
import android.os.Handler
import android.widget.ProgressBar
import kotlinx.coroutines.delay
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

import org.java_websocket.client.WebSocketClient
import org.java_websocket.handshake.ServerHandshake
import java.net.URI
import java.security.SecureRandom
import java.security.cert.X509Certificate
import java.util.Dictionary
import javax.net.ssl.SSLContext
import javax.net.ssl.TrustManager
import javax.net.ssl.X509TrustManager

@Serializable
data class Authorization(val action: String, val wearableID: String, val secret: String)
@Serializable
data class Heartbeat(val action: String)
@Serializable
data class OrderMessage(val action: String, val wearableID: String, val sensorVal: String)

class CheckoutActivity : AppCompatActivity() {
    private lateinit var endButton: ImageButton
    private var webSocketClient: WebSocketClient? = null
    private lateinit var textView: TextView
    private lateinit var progressBar: ProgressBar
    private val handler = Handler()
    val WID = "gp20906498"
    val AKEY = "gp57277569125c1b08"
    private val heartbeatRunnable = object : Runnable {
        override fun run() {
            sendHeartbeat()
            Log.e("heartbeat", "heartbeat")
            handler.postDelayed(this, 30000) // Schedule this again in 50 seconds
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_checkout)

        endButton = findViewById(R.id.endButton)
        textView = findViewById(R.id.textView4)
        progressBar = findViewById(R.id.progressBar)
        connectToGyroPalmServer()

        endButton.setOnClickListener {
            val mainActivityIntent = Intent(this, MainActivity::class.java)
            startActivity(mainActivityIntent)
            webSocketClient?.close()
        }
    }

    private fun connectToGyroPalmServer() {
        try {
            val uri = URI("wss://gyropalm.com:3200")
            webSocketClient = createWebSocketClient(uri)
            webSocketClient?.connect()
        } catch (e: Exception) {
            Log.e("Websocket", "Exception: ${e.message}")
            e.printStackTrace()
        }
    }

    private fun createWebSocketClient(uri: URI): WebSocketClient {
        val sslContext = SSLContext.getInstance("TLS")
        sslContext.init(null, arrayOf<TrustManager>(object : X509TrustManager {
            override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
            override fun checkClientTrusted(chain: Array<X509Certificate>, authType: String) {}
            override fun checkServerTrusted(chain: Array<X509Certificate>, authType: String) {}
        }), SecureRandom())

        val socketFactory = sslContext.socketFactory

        return object : WebSocketClient(uri) {
            override fun onOpen(serverHandshake: ServerHandshake) {
                Log.i("Websocket", "Opened")
                val authMessage = Json.encodeToString(Authorization("new", WID, AKEY))
                send(authMessage)

            }

            override fun onMessage(message: String) {
                runOnUiThread {
                    try {
                        val jsonObject = Json.parseToJsonElement(message).jsonObject
                        val action = jsonObject["action"]?.jsonPrimitive?.content
                        val orderString = "{\\\"order\\\":\\\"" + intent.getStringExtra("order") + "\\\"}"

                        Log.e("Connection", message)
                        when (action) {
                            "info" -> handleInfoAction(jsonObject)
                            "data" -> handleDataAction(jsonObject)
                            else -> Log.i("Websocket", "Unknown action: $action")
                        }
                    } catch (e: Exception) {
                        Log.e("Websocket", "Error parsing message: ${e.message}")
                    }
                }
            }

            private fun handleInfoAction(jsonObject: JsonObject) {
                val stat = jsonObject["stat"]?.jsonPrimitive?.content
                if (stat == "success") {
                    handler.postDelayed(heartbeatRunnable, 30000) // Schedule this again in 50 seconds
                    val orderString = intent.getStringExtra("order").toString().replace("\n", "").replace(" ","")
                    val orderJSON = Json.encodeToString(OrderMessage("pub", WID, orderString))
                    sendJsonMessage(orderJSON)
                }
                // Implement logic for "info" action
            }

            private fun handleDataAction(jsonObject: JsonObject) {
                // Implement logic for "data" action
                val command = jsonObject["command"]?.jsonPrimitive?.content
                val number = command?.toInt()
                if (number != null) {
                    if (number <= 25) {
                        textView.text = "Robot on the way to fulfillment station! ...$number%"
                    } else if(number <= 50) {
                        textView.text = "Loading items on the Robot! ...$number%"
                    } else if (number <= 75) {
                        textView.text = "Robot on the way to the delivery station! ...$number%"
                    } else if (number >= 97) {
                        textView.text = "Your order is arriving! ...$number%"
                    } else if (number == 100) {
                        textView.text = "Order Complete! ...100%"
                    }
                }
            }

            override fun onClose(code: Int, reason: String, remote: Boolean) {
                Log.i("Websocket", "Closed $reason")
                handler.removeCallbacks(heartbeatRunnable) // Stop sending heartbeats
            }

            override fun onError(ex: Exception) {
                Log.e("Websocket", "Error ${ex.message}")
            }

            init {
                if (uri.scheme.equals("wss", ignoreCase = true)) {
                    setSocketFactory(socketFactory)
                }
            }
        }
    }

    private fun sendHeartbeat() {
        val heartbeatMessage = Json.encodeToString(Heartbeat("heartbeat"))
        sendJsonMessage(heartbeatMessage)
    }



    fun sendJsonMessage(jsonMessage: String) {
        if (webSocketClient?.isOpen == true) {
            webSocketClient?.send(jsonMessage)
        } else {
            Log.e("Websocket", "WebSocket is not connected.")
        }
    }
}
