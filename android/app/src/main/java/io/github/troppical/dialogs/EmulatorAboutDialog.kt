package io.github.troppical.dialogs

import android.content.Context
import android.os.Bundle
import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.CompoundButton
import android.widget.ImageView
import android.widget.TextView
import com.bumptech.glide.Glide
import kotlinx.coroutines.*
import io.github.troppical.R
import io.github.troppical.network.GitHubReleaseFetcher

class EmulatorAboutDialog(context: Context, private val item: HashMap<String, Any>) : BaseSheetDialog(context) {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.emulator_about_dialog)

        val emulatorName = findViewById<TextView>(R.id.emulator_name)
        val emulatorDesc = findViewById<TextView>(R.id.emulator_desc)
        val emulatorLogo = findViewById<ImageView>(R.id.emulator_logo)
        val emulatorLatestVersion = findViewById<TextView>(R.id.emulator_latest_version)

        emulatorLatestVersion.text = tagName
        emulatorName.text = item["emulator_name"].toString()
        emulatorDesc.text = item["emulator_desc"].toString()
        Glide.with(context).load(Uri.parse(item["emulator_logo"].toString())).into(emulatorLogo)

        // Fetch the latest version information asynchronously
        GlobalScope.launch(Dispatchers.Main) {
            val fetcher = GitHubReleaseFetcher(item["emulator_owner"].toString(), item["emulator_repo"].toString())
            try {
                val artifactName = item["emulator_artifact_name"].toString()
                val (directLink, tagName) = fetcher.fetchArtifactDirectLinkAndTag(artifactName)
                // Update the UI with the fetched tag name
                emulatorLatestVersion.text = tagName
            } catch (e: Exception) {
                // Handle any errors here
                emulatorLatestVersion.text = "Error fetching version"
            } finally {
                fetcher.close()
            }
        }  
    }
}
