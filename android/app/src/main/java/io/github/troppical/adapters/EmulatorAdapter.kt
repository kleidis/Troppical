package io.github.troppical.adapters

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView
import android.net.Uri
import com.bumptech.glide.Glide
import com.google.android.material.card.MaterialCardView
import io.github.troppical.R
import io.github.troppical.dialogs.EmulatorAboutDialog

class EmulatorAdapter(private val context: Context, private val data: ArrayList<HashMap<String, Any>>) : BaseAdapter() {

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

        val card_emulator = view.findViewById<MaterialCardView>(R.id.card_emulator)
        val emulator_logo = view.findViewById<ImageView>(R.id.emulator_logo)
        val emulator_name = view.findViewById<TextView>(R.id.emulator_name)
        val emulator_desc = view.findViewById<TextView>(R.id.emulator_desc)

        val item = getItem(position)
        emulator_name.text = item["emulator_name"].toString()
        emulator_desc.text = item["emulator_desc"].toString()
        Glide.with(context).load(Uri.parse(item["emulator_logo"].toString())).into(emulator_logo)

        card_emulator.setOnClickListener {
           val dialog = EmulatorAboutDialog(context, item)
           dialog.show()
        }

        return view
    }
}
