package io.github.troppical.dialogs

import android.content.Context
import android.os.Bundle
import android.net.Uri
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.CompoundButton
import android.widget.ImageView
import android.widget.TextView
import com.bumptech.glide.Glide
import com.google.android.material.button.MaterialButton
import kotlinx.coroutines.*
import io.github.troppical.R
import io.github.troppical.network.GitHubReleaseFetcher
import io.github.troppical.network.APKDownloader
import io.github.troppical.network.APKInstaller
import java.io.File

class EmulatorAboutDialog(context: Context, private val item: HashMap<String, Any>) : BaseSheetDialog(context) {

    private val fetcherScope = CoroutineScope(Dispatchers.Main + Job())
    private lateinit var downloadUrl: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.emulator_about_dialog)

        val emulatorName = findViewById<TextView>(R.id.emulator_name)
        val emulatorDesc = findViewById<TextView>(R.id.emulator_desc)
        val emulatorLogo = findViewById<ImageView>(R.id.emulator_logo)
        val emulatorLatestVersion = findViewById<TextView>(R.id.emulator_latest_version)
        val installButton = findViewById<MaterialButton>(R.id.install)

        emulatorName.text = item["emulator_name"].toString()
        emulatorDesc.text = item["emulator_desc"].toString()
        Glide.with(context).load(Uri.parse(item["emulator_logo"].toString())).into(emulatorLogo)

        fetcherScope.launch {
            val fetcher = GitHubReleaseFetcher(item["emulator_owner"].toString(), item["emulator_repo"].toString())
            try {
                val artifactName = item["emulator_artifact_name"].toString()
                val (directLink, tagName) = fetcher.fetchArtifactDirectLinkAndTag(artifactName)
                // Update the UI with the fetched tag name
                emulatorLatestVersion.text = tagName

                if (directLink != null) {
                    downloadUrl = directLink 
                    Log.w("EmulatorAboutDialog", "Direct download link is $directLink")
                } else {
                    Log.e("EmulatorAboutDialog", "Artifact not found")
                }
            } catch (e: Exception) {
                // Log the error to understand what went wrong
                Log.e("EmulatorAboutDialog", "Error fetching version", e)
                emulatorLatestVersion.text = "Error fetching version"
            } finally {
                fetcher.close()
            }
        }
        
        installButton.setOnClickListener {
          if (downloadUrl != null) {
              val outputFile = File(context.filesDir, item["emulator_artifact_name"].toString())
              val downloader = APKDownloader(downloadUrl, outputFile)
              downloader.download { success ->
                  if (success) {
                      val installer = APKInstaller(context)
                      installer.install(outputFile)
                  } else {
                      // TODO: Handle download failure
                  }
              } 
           }     
        }          
    }

    override fun onStop() {
        super.onStop()
        fetcherScope.cancel() // Cancel any ongoing coroutines when the dialog is destroyed
    }
}
