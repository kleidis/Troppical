package io.github.troppical.dialogs

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.widget.LinearLayout
import com.google.android.material.bottomsheet.BottomSheetDialog
import io.github.troppical.R
import io.github.troppical.utils.CompatUtils

open class BaseSheetDialog(context: Context) : BottomSheetDialog(CompatUtils.findActivity(context)) {
    private val contentView: LinearLayout

    init {
        val width = CompatUtils.findActivity(context).window.decorView.measuredWidth
        val height = CompatUtils.findActivity(context).window.decorView.measuredHeight
        val heightScale = 0.87f // What percentage of the screen's height to use up

        behavior.peekHeight = (height * heightScale).toInt()
        behavior.maxHeight = (height * heightScale).toInt()
        behavior.maxWidth = width

        super.setContentView(R.layout.base_sheet_dialog)
        contentView = super.findViewById(R.id.content)!!
    }

    override fun setContentView(view: View) {
        contentView.removeAllViews()
        contentView.addView(view)
    }

    override fun setContentView(layoutResID: Int) {
        setContentView(LayoutInflater.from(context).inflate(layoutResID, null, false))
    }

    override fun <T : View?> findViewById(id: Int): T {
        return contentView.findViewById<T>(id)!!
    }
}