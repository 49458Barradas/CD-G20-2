import java.io.*
import java.net.*

const val HTTPPORT = 80

enum class HTTPMethods{
    GET, HEAD, PATCH, POST, PUT, OPTIONS, DELETE
}

fun accessIt(httpRequest: httpRequest, requestTypeInput: HTTPMethods?){
    val requestType: HTTPMethods = requestTypeInput ?: getHTTPRequestType()

    val host = httpRequest.host
    val path: String = httpRequest.path

    val socket = Socket(host, HTTPPORT)
    val outputStream = socket.getOutputStream()

    var request = "Evitar Erro"
    if(requestType==HTTPMethods.GET||requestType==HTTPMethods.HEAD||requestType==HTTPMethods.OPTIONS){
        request = "$requestType $path HTTP/1.1\r\n" +
                "Host: $host\r\n" +
                "\r\n"
    }
    if(requestType==HTTPMethods.PATCH||requestType==HTTPMethods.POST||requestType==HTTPMethods.PUT){
        println("Insert name of file you want to POST or PATCH: ")
        print("-> ")
        val file = File(readln())
        println()
        println("Insert data for body of request: ")
        print("-> ")
        val body = readln()
        request = "$requestType $path HTTP/1.1\r\n" +
                "Host: $host\r\n" +
                "Content-type: ${URLConnection.guessContentTypeFromName(file.name)} \r\n" +
                "Content-Length: ${file.length()}" +
                body +
                "\r\n"
    }
    if(requestType==HTTPMethods.DELETE){
            println("Insert ID of resource you want to delete:")
            print("-> ")
            val resourceId= readln()
            request = "$requestType $path/$resourceId HTTP/1.1\r\n" +
                    "Host: $host\r\n" +
                    "\r\n"
    }
    outputStream.write(request.toByteArray())
    outputStream.flush()

    val inputStream = socket.getInputStream()
    val buffer = ByteArray(4096)
    var bytesRead: Int

    val response = StringBuilder()

    // Read the response from the server
    while (inputStream.read(buffer).also { bytesRead = it } != -1) {
        response.append(String(buffer, 0, bytesRead))
    }

    when (response.split("\n")[0].substring("HTTP/1.1 ".length).trimEnd('\r').lowercase()) {
        "302 found" -> {
            socket.close()
            val urlInput = userInput(response.split("\n")[4].substring("Location: ".length).trimEnd('\r'))
            accessIt(urlInput, requestType)
        }
        "200 ok" -> {
            println(response.toString())

            socket.close()
        }
        else -> println("An unexpected error occurred")
    }
}

fun getHTTPRequestType(): HTTPMethods{
    println("What type of HTTP Request would you like to use: ")
    println("1 - GET")
    println("2 - HEAD")
    println("3 - PATCH")
    println("4 - POST")
    println("5 - PUT")
    println("6 - OPTIONS")
    println("7 - DELETE")
    var userInput: HTTPMethods? = null
    while (userInput == null){
        print("-> ")
        when (readln().toIntOrNull()) {
            1 -> userInput = HTTPMethods.GET
            2 -> userInput = HTTPMethods.HEAD
            3 -> userInput = HTTPMethods.PATCH
            4 -> userInput = HTTPMethods.POST
            5 -> userInput = HTTPMethods.PUT
            6 -> userInput = HTTPMethods.OPTIONS
            7 -> userInput = HTTPMethods.DELETE
            null -> println("Invalid input, try again.")
        }
    }
    return userInput
}

enum class TwoType{
    WITH, WITHOUT
}

data class httpRequest(val host: String, val path: String)

fun urlInput() :httpRequest{
    print("URL Input: ")
    val url = readln()
    return userInput(url)
}

fun userInput(url:String): httpRequest {
    val http = "http://"
    var urlType: TwoType = TwoType.WITH
    for (i in http.indices) {
        if (url[i] != http[i]) urlType = TwoType.WITHOUT
    }
    if (urlType == TwoType.WITH) {
        val newURL = url.substring(http.length)
        val temp = newURL.split("/")
        val host = temp[0]
        val temp1 = temp[1].split("?")
        val path = "/" + temp1[0] + "/"
        /*
        var query = ""
        if (temp1.size != 1) {
            for (i in 1 until temp1.size) {
                query += temp[i]
            }
        }
         */
        return httpRequest(host, path)
    } else {
        val temp = url.split("/")
        val host = temp[0]
        val temp1 = temp[1].split("?")
        val path = "/" + temp1[0] + "/"
        /*
        var query = ""
        if (temp1.size != 1) {
            for (i in 1 until temp1.size) {
                query += temp[i]
            }
        }
         */
        println("WITHOUT")
        println(temp)
        println(host)
        println(path)
        return httpRequest(host, path)
    }
}

fun main(){
    while(true) {
        val urlInput = urlInput()

        accessIt(urlInput, null)
    }
}
