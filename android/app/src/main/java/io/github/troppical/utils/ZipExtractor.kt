package io.github.troppical.utils

import java.io.*
import java.util.zip.ZipEntry
import java.util.zip.ZipInputStream

class ZipExtractor(
    private val zipFilePath: String, 
    private val destDirectory: String, 
    private val progressCallback: (Int) -> Unit,
    private val onComplete: (Boolean, String?) -> Unit
) {

    private val extractedFiles = mutableListOf<String>()
    var apkFilePath: String? = null
        private set
    var isExtractionDone: Boolean = false
        private set

    fun extract() {
        val destDir = File(destDirectory)
        if (!destDir.exists()) {
            destDir.mkdirs()
        }

        try {
            FileInputStream(zipFilePath).use { fis ->
                val totalSize = fis.available()
                var extractedSize = 0

                ZipInputStream(fis).use { zipIn ->
                    var entry: ZipEntry? = zipIn.nextEntry
                    while (entry != null) {
                        val filePath = destDirectory + File.separator + entry.name
                        if (!entry.isDirectory) {
                            // Extract the file
                            val fileSize = extractFile(zipIn, filePath)
                            extractedFiles.add(filePath)
                            // Check if it's an APK file
                            if (filePath.endsWith(".apk", ignoreCase = true)) {
                                apkFilePath = filePath
                            }
                            extractedSize += fileSize
                            val progress = (extractedSize.toDouble() / totalSize * 100).toInt()
                            progressCallback(progress)
                        } else {
                            // Create the directory
                            val dir = File(filePath)
                            dir.mkdirs()
                            extractedFiles.add(filePath + File.separator)
                        }
                        zipIn.closeEntry()
                        entry = zipIn.nextEntry
                    }
                    isExtractionDone = true
                    onComplete(true, apkFilePath)
                }
            }
        } catch (e: IOException) {
            e.printStackTrace()
            isExtractionDone = false
            onComplete(false, null)
        }
    }

    @Throws(IOException::class)
    private fun extractFile(zipIn: ZipInputStream, filePath: String): Int {
        var fileSize = 0
        BufferedOutputStream(FileOutputStream(filePath)).use { bos ->
            val bytesIn = ByteArray(BUFFER_SIZE)
            var read: Int
            while (zipIn.read(bytesIn).also { read = it } != -1) {
                bos.write(bytesIn, 0, read)
                fileSize += read
            }
        }
        return fileSize
    }

    fun getExtractedFiles(): List<String> {
        return extractedFiles
    }

    companion object {
        private const val BUFFER_SIZE = 4096 // Buffer size for reading/writing data
    }
}
