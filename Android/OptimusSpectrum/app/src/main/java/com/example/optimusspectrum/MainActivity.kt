package com.example.optimusspectrum

import android.content.Intent
import android.os.Bundle
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast

import androidx.appcompat.app.AppCompatActivity


class MainActivity : AppCompatActivity() {
    private lateinit var text: TextView
    // Add button Move to Activity
    private lateinit var product1: ImageButton
    private lateinit var product2: ImageButton
    private lateinit var product3: ImageButton
    private lateinit var product4: ImageButton
    private lateinit var delete: ImageButton
    private lateinit var order: ImageButton

    var orderList = mutableListOf<String>(",")
    var sendList = mutableListOf<String>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        product1 =  findViewById(R.id.product1)
        product2 =  findViewById(R.id.product2)
        product3 =  findViewById(R.id.product3)
        product4 =  findViewById(R.id.product4)
        order = findViewById(R.id.orderButton)
        delete = findViewById(R.id.deleteButton)
        text = findViewById(R.id.textView2)

        product1.setOnClickListener {
            if (orderList.count() <= 4){
                orderList.add("Red\n")
                text.text = orderList.toString().trim('[').trim(']').filterNot { it == ',' }.trimIndent()
            }
            else {
                val toast = Toast.makeText(this, "Max Items Added To Cart!", Toast.LENGTH_LONG) // in Activity
                toast.show()
            }

        }

        product2.setOnClickListener {
            if (orderList.count() <= 4){
                orderList.add("Blue\n")
                text.text = orderList.toString().trim('[').trim(']').filterNot { it == ',' }.trimIndent()
            }
            else {
                val toast = Toast.makeText(this, "Max Items Added To Cart!", Toast.LENGTH_LONG) // in Activity
                toast.show()

            }
        }

        product3.setOnClickListener {
            if (orderList.count() <= 4){
                orderList.add("Green\n")
                text.text = orderList.toString().trim('[').trim(']').filterNot { it == ',' }.trimIndent()
            }
            else {
                val toast = Toast.makeText(this, "Max Items Added To Cart!", Toast.LENGTH_LONG) // in Activity
                toast.show()
            }
        }

        product4.setOnClickListener {
            if (orderList.count() <= 4){
                orderList.add("Black\n")
                text.text = orderList.toString().trim('[').trim(']').filterNot { it == ',' }.trimIndent()
            }
            else {
                val toast = Toast.makeText(this, "Max Items Added To Cart!", Toast.LENGTH_SHORT) // in Activity
                toast.show()
            }
        }

        delete.setOnClickListener{
            if(orderList.size != 1) {
                orderList.removeLast()
                if (orderList.size == 1){
                    text.text = "Cart is Empty"
                }
                else {
                    text.text = orderList.toString().trim('[').trim(']').filterNot { it == ',' }
                        .trimIndent()
                }
            }
            else {
                val toast = Toast.makeText(this, "No Items In Cart!", Toast.LENGTH_SHORT) // in Activity
                toast.show()
            }
        }

        order.setOnClickListener{
            val checkoutActivity = Intent(
                this@MainActivity,
                CheckoutActivity::class.java
            )
            for (i in orderList){
                sendList.add(i.trim('\n'))
            }
            var list_text = sendList.toString().trim('[').trim(']').trim(',').trim(' ')
            checkoutActivity.putExtra("order", list_text)
            startActivity(checkoutActivity)
        }
    }
}

