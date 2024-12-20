To decode a Base64 string and map the value of a specific key from the decoded JSON in WireMock, you can use **Handlebars templating** in combination with the `base64Decode` helper and the `jsonPath` helper.

### **Steps**

1. **Decode the Base64 string**.
2. **Parse the decoded string as JSON**.
3. **Extract the value of a specific key from the JSON**.

In this solution, you will leverage WireMock's Handlebars helpers and `jsonPath` to achieve this transformation.

### **Solution Using Handlebars Templating**

Here’s an example:

### **1. Mapping File Example (`base64-header-mapping.json`)**

```json
{
  "request": {
    "method": "GET",
    "urlPath": "/example"
  },
  "response": {
    "status": 200,
    "body": "{{#if (exists request.headers.X-Custom-Header)}}{{#with (jsonPath (base64Decode request.headers.X-Custom-Header.[0]) '$.desiredKey')}}{{this}}{{else}}Key not found in decoded JSON{{/with}}{{else}}Missing header{{/if}}",
    "headers": {
      "Content-Type": "application/json"
    },
    "transformers": ["response-template"]
  }
}
```

### **Explanation**

1. **Check Header Existence**:
   - `{{exists request.headers.X-Custom-Header}}`: Verifies that the `X-Custom-Header` exists in the request.

2. **Decode Base64**:
   - `{{base64Decode request.headers.X-Custom-Header.[0]}}`: Decodes the Base64 string found in the `X-Custom-Header`.

3. **Parse JSON**:
   - `{{jsonPath (base64Decode ...) '$.desiredKey'}}`: Uses `jsonPath` to extract the value associated with the key `desiredKey` from the decoded JSON string.

4. **Handle Missing Header or Key**:
   - The template includes checks for both missing headers and missing keys in the decoded JSON.

### **2. Example of the Base64 Encoded Header**

Given that the header contains a Base64 encoded string, the value might look something like this:

**Header Example**:
```http
X-Custom-Header: eyJkZXNpcmVkS2V5IjoiZXhhbXBsZVZhbHVlIn0=  # Base64 of {"desiredKey": "exampleValue"}
```

When decoded, the value is:
```json
{
  "desiredKey": "exampleValue"
}
```

### **3. Response Body**

When you access `/example` with the request above, WireMock will decode the Base64 string, parse it as JSON, and return the value associated with `desiredKey`:

#### Response Body:
```json
"exampleValue"
```

### **4. Additional Notes**

- **Base64 Decode**: `{{base64Decode request.headers.X-Custom-Header.[0]}}` decodes the Base64 string.
- **JSON Path**: `{{jsonPath (base64Decode ...) '$.desiredKey'}}` is used to extract the value associated with `desiredKey` from the decoded JSON.
- **Error Handling**: If the header is missing, the response will include `"Missing header"`. If the key is not found in the decoded JSON, the response will include `"Key not found in decoded JSON"`.

### **5. Enable Response Templating**

Make sure that response templating is enabled in WireMock.

#### Command-line Example:
```bash
java -jar wiremock-standalone.jar --global-response-templating
```

Alternatively, if you are using Spring Boot, ensure you have the response template transformer configured:

#### Spring Boot Configuration:
```java
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;
import com.github.tomakehurst.wiremock.extension.responsetemplating.ResponseTemplateTransformer;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class WireMockApplication {

    public static void main(String[] args) {
        SpringApplication.run(WireMockApplication.class, args);
    }

    @Bean
    public WireMockConfiguration wireMockConfig() {
        return WireMockConfiguration.wireMockConfig()
                .extensions(new ResponseTemplateTransformer(true));
    }
}
```

---

### **6. Test the Implementation**

#### Request:

```http
GET /example HTTP/1.1
Host: localhost:8080
X-Custom-Header: eyJkZXNpcmVkS2V5IjoiZXhhbXBsZVZhbHVlIn0=  # Base64 of {"desiredKey": "exampleValue"}
```

#### Response Body:

```json
"exampleValue"
```

### **Conclusion**

By using **Handlebars** and **WireMock’s built-in helpers**, you can easily decode a Base64 string, parse it as JSON, and access specific keys in the decoded content directly within your WireMock mappings. This makes it easier to create dynamic responses based on incoming request data.
