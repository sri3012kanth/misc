In Spring Boot, you can use the HTTP Interface feature introduced in Spring Framework 6.1 and Spring Boot 3.2 to define HTTP clients in a declarative way, similar to Retrofit. Here’s how to do it:

Step 1: Add Dependencies

Ensure your pom.xml or build.gradle includes the following dependencies:

Maven

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

Gradle

implementation 'org.springframework.boot:spring-boot-starter-web'

Step 2: Enable HTTP Interfaces in Spring Boot

Add the @EnableHttpInterfaces annotation in your Spring Boot configuration class to enable HTTP interface support.

@Configuration
@EnableHttpInterfaces
public class AppConfig {
}

Step 3: Define an HTTP Interface

Create an interface to represent your REST API endpoints. Use Spring MVC-style annotations to define the HTTP methods and endpoints.

@HttpExchange("/api/resource")
public interface MyApiClient {

    @GetExchange("/{id}")
    MyResponse getResource(@PathVariable String id);

    @PostExchange
    MyResponse createResource(@RequestBody MyRequest request);
}

	•	@HttpExchange: Defines the base path for the API.
	•	@GetExchange, @PostExchange, etc.: Define HTTP methods (similar to @GetMapping, @PostMapping).
	•	@PathVariable, @RequestBody, etc.: Bind path parameters or request bodies.

Step 4: Register the HTTP Client Bean

Spring Boot will automatically create an implementation of the interface. Register it as a bean by declaring it in your configuration.

@Configuration
@EnableHttpInterfaces
public class AppConfig {

    @Bean
    public MyApiClient myApiClient(HttpInterfaceFactory factory) {
        return factory.createClient(MyApiClient.class);
    }
}

Alternatively, you can directly inject the interface into your services if you’re using Spring Boot 3.2+.

Step 5: Use the HTTP Interface

Inject and use the MyApiClient wherever needed in your application.

@Service
public class MyService {

    private final MyApiClient myApiClient;

    public MyService(MyApiClient myApiClient) {
        this.myApiClient = myApiClient;
    }

    public MyResponse getResource(String id) {
        return myApiClient.getResource(id);
    }

    public MyResponse createResource(MyRequest request) {
        return myApiClient.createResource(request);
    }
}

Example Classes

Request and Response DTOs

public class MyRequest {
    private String name;
    private String description;
    // Getters and setters
}

public class MyResponse {
    private String id;
    private String name;
    private String description;
    // Getters and setters
}

Advantages of Using HTTP Interfaces
	1.	Declarative and Clean: Define endpoints directly in interfaces without needing boilerplate code.
	2.	Built-in Support: No need for third-party libraries; it’s supported natively in Spring.
	3.	Integration with Spring Features: Works seamlessly with other Spring annotations and features.

This approach provides a Retrofit-like experience while staying within the Spring ecosystem.