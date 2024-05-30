package io.github.troppical

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.GridView
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import io.github.troppical.network.RequestNetwork
import io.github.troppical.network.RequestNetworkController
import io.github.troppical.adapters.EmulatorAdapter

class MainActivity : AppCompatActivity() {

    private var listmap: ArrayList<HashMap<String, Any>> = ArrayList()
    private lateinit var netRequestListener: RequestNetwork.RequestListener

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_activity)

        netRequestListener = object : RequestNetwork.RequestListener {
            override fun onResponse(_param1: String, _param2: String, _param3: HashMap<String, Any>) {
                val _response = _param2
                listmap = Gson().fromJson(_response, object : TypeToken<ArrayList<HashMap<String, Any>>>() {}.type)
                val gridEmulators: GridView = findViewById(R.id.grid_emulators)
                gridEmulators.adapter = EmulatorAdapter(this@MainActivity, listmap)
            }

            override fun onErrorResponse(_param1: String, _param2: String) {
                // TODO: Handle this situation
            }
        }

        val net = RequestNetwork(this)
        net.startRequestNetwork(
            RequestNetworkController.GET, 
            "https://script.googleusercontent.com/macros/echo?user_content_key=Hw-G9S_OHELhOUAsT-oQr8ux2HPMIpva3U1w0Su7P1ZYrr1ngXyqlN6LBhfev1taFoRtJ07w_KDhWVbMaBaeJ3c86H4e0k8Xm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnL69XsVZDOhipZMwrhs3JioNozSVnp4Chm6SveAF_nlUSMgTaOh-zk0bQ5F9LtyaiRZKic-heYuYVV866SySaVfv-0TkTPKcCtz9Jw9Md8uu&lib=MmjrdpKGbUxdyxLDAqWkoFhoZjK-0W8qS",
            "",
            netRequestListener
        )
    }
}
