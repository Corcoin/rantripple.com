library(httr)

# Proxy server details
proxy_host <- "your_proxy_host"
proxy_port <- your_proxy_port
proxy_url <- paste0("http://", proxy_host, ":", proxy_port)

# HTTP GET request through proxy
response <- GET("http://www.example.com", 
               config = httr::use_proxy(url = proxy_url))
               
# Check response
status_code(response)  # HTTP status code
content(response, "text")  # Content of the response
