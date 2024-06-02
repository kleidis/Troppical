package io.github.troppical.utils

import android.app.Activity
import android.content.Context
import android.content.ContextWrapper

object CompatUtils {
    fun findActivity(context: Context): Activity {
        return when (context) {
            is Activity -> context
            is ContextWrapper -> findActivity(context.baseContext)
            else -> throw IllegalArgumentException("Context is not an Activity")
        }
    }
}