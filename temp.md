To dynamically drive the transformation through a template-based response in JSON, you can use **WireMock’s Handlebars templating engine**. Handlebars templates allow you to manipulate request data, such as headers, directly in the response.

Here’s how to achieve this with a template-driven approach:

---

### **Steps to Access Base64 Encoded Header Value in the Response**

1. **Enable Global Response Templating**:
   - Configure WireMock to enable response templating.

2. **Define a Mapping with Handlebars**:
   - Use Handlebars helpers to manipulate the header data in the mapping file.

3. **Customize the Header Logic**:
   - Decode the base64 header, split it by a colon (`:`), and extract the desired part.

---

### **Mapping File Example**

Create a mapping file that uses Handlebars templates to decode the base64 header.

`mappings/base64-header-mapping.json`:
```json
{
  "request": {
    "method": "GET",
    "urlPath": "/example"
  },
  "response": {
    "status": 200,
    "body": "{{#if (exists request.headers.X-Custom-Header)}}{{#with (base64Decode request.headers.X-Custom-Header.[0])}}{{split this ':' 1}}{{else}}Missing or invalid header{{/with}}{{else}}Missing header{{/if}}",
    "headers": {
      "Content-Type": "application/json"
    },
    "transformers": ["response-template"]
  }
}
```

---

### **Explanation of the Template**

1. **Check Header Existence**:
   - `{{exists request.headers.X-Custom-Header}}`: Ensures the header exists.

2. **Decode the Base64 Header**:
   - `{{base64Decode request.headers.X-Custom-Header.[0]}}`: Decodes the first value of the `X-Custom-Header`.

3. **Split by Colon**:
   - `{{split this ':' 1}}`: Splits the decoded string on `:` and retrieves the second part.

4. **Handle Missing Values**:
   - The `{{#if}}` and `{{else}}` blocks ensure appropriate fallback messages for missing or invalid headers.

---

### **Enable Global Response Templating**

To enable global response templating, you need to configure WireMock with the `--global-response-templating` flag.

#### Command:
```bash
java -jar wiremock-standalone.jar --global-response-templating
```

---

### **Test the Endpoint**

#### Request:
```http
GET /example HTTP/1.1
Host: localhost:8080
X-Custom-Header: QWJjZGVmZzpoaWprbG1ub3A=
```

#### Response:
```json
{
  "property": "hijklmnop"
}
```

---

### **Optional: Run WireMock in Spring Boot**

If migrating to Spring Boot, you can leverage the same `response-template` transformer by enabling it programmatically.

#### Spring Boot Configuration Example:

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

### **Key Advantages**

1. **Dynamic Response Handling**:
   - No need for custom Java code; logic is handled directly in the template.

2. **Ease of Configuration**:
   - Makes mappings more declarative and easier to maintain.

3. **Flexible Logic**:
   - Handlebars helpers allow for complex transformations without extra programming.

This approach lets you handle dynamic logic directly in the response JSON, making it ideal for templated and flexible testing scenarios.
