package io.github.troppical.adapters

import android.content.Context
import android.os.SystemClock
import android.view.LayoutInflater
import android.view.View
import android.app.Activity
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.text.TextUtils
import android.net.Uri
import com.bumptech.glide.Glide
import com.google.android.material.card.MaterialCardView
import io.github.troppical.R
import io.github.troppical.dialogs.EmulatorAboutDialog

class EmulatorAdapter(private val context: Context, private val activity: Activity, private val data: ArrayList<HashMap<String, Any>>) : BaseAdapter() {

    private var lastClickTime = 0L
    
    override fun getCount(): Int {
        return data.size
    }

    override fun getItem(position: Int): HashMap<String, Any> {
        return data[position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val inflater = LayoutInflater.from(context)
        val view = convertView ?: inflater.inflate(R.layout.card_emulator, parent, false)

        val cardEmulator = view.findViewById<MaterialCardView>(R.id.card_emulator)
        val emulatorLogo = view.findViewById<ImageView>(R.id.emulator_logo)
        val emulatorName = view.findViewById<TextView>(R.id.emulator_name)
        val emulatorDesc = view.findViewById<TextView>(R.id.emulator_desc)

        val item = getItem(position)
        emulatorName.text = item["emulator_name"].toString()
        emulatorDesc.text = item["emulator_desc"].toString()
        Glide.with(context).load(Uri.parse(item["emulator_logo"].toString())).into(emulatorLogo)
        
        emulatorDesc.ellipsize = TextUtils.TruncateAt.MARQUEE
        emulatorDesc.isSelected = true

        cardEmulator.setOnClickListener {
           // Double-click prevention, using threshold of 1000 ms
           if (SystemClock.elapsedRealtime() - lastClickTime < 1000) {
               return@setOnClickListener
           }
           lastClickTime = SystemClock.elapsedRealtime()
        
           val dialog = EmulatorAboutDialog(context, activity, item)
           dialog.show()
        }

        return view
    }
}
