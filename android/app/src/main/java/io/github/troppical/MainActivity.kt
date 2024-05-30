package io.github.troppical

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.appcompat.app.androidx.appcompat.app.AppCompatActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import io.github.troppical.ui.theme.TroppicalTheme
import io.github.troppical.network.RequestNetwork
import io.github.troppical.network.RequestNetworkController

class MainActivity : AppCompatActivity {

    private var listmap: ArrayList<HashMap<String, Any>> = ArrayList()
    private lateinit var netRequestListener: RequestNetwork.RequestListener 


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main_activity)

        val net = object : RequestNetwork(this)

        val grid_emulators = findViewById(R.id.grid_emulators)

        net.startRequestNetwork(RequestNetworkController.GET, "https://script.googleusercontent.com/macros/echo?user_content_key=Hw-G9S_OHELhOUAsT-oQr8ux2HPMIpva3U1w0Su7P1ZYrr1ngXyqlN6LBhfev1taFoRtJ07w_KDhWVbMaBaeJ3c86H4e0k8Xm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnL69XsVZDOhipZMwrhs3JioNozSVnp4Chm6SveAF_nlUSMgTaOh-zk0bQ5F9LtyaiRZKic-heYuYVV866SySaVfv-0TkTPKcCtz9Jw9Md8uu&lib=MmjrdpKGbUxdyxLDAqWkoFhoZjK-0W8qS", "", netRequestListener)

        netRequestListener = object : RequestNetwork.RequestListener {
           override fun onResponse(_param1: String, _param2: String, _param3: HashMap<String, Any>) {
               val _tag = _param1
               val _response = _param2
               val _responseHeaders = _param3
               listmap = Gson().fromJson(_response, object : TypeToken<ArrayList<HashMap<String, Any>>>() {}.type)
               grid_emulators.adapter = EmulatorAdapter(this@MainActivity, listmap)
            }

            override fun onErrorResponse(_param1: String, _param2: String) {
                val _tag = _param1
                val _message = _param2
                // TODO: Handle this situation
            }

        }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    }

}