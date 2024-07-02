package io.github.troppical.utils

class Task : Thread {
    constructor(runnable: Runnable) : super(runnable)

    protected constructor()

    fun runSync() {
        start()
        waitFinish()
    }

    fun waitFinish() {
        try {
            join()
        } catch (e: InterruptedException) {
            throw RuntimeException(e)
        }
    }
}
