Here's a **JUnit 5 + MockK** test for your `MigrateDryRunClientInterceptor` class. It mocks the dependencies and verifies the behavior of the `interceptCall` method.

### Test Case:
- Ensures that `interceptCall` correctly passes `callOptions` to `next.newCall`.
- Verifies that the metadata header `IS_DRY_RUN_METADATA_KEY` is set correctly in `start`.
- Uses MockK for mocking the `Channel`, `MethodDescriptor`, and other dependencies.

---

### **Test Implementation:**
```kotlin
import io.grpc.*
import io.mockk.*
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class MigrateDryRunClientInterceptorTest {

    private lateinit var interceptor: MigrateDryRunClientInterceptor
    private lateinit var mockChannel: Channel
    private lateinit var mockCall: ClientCall<Any, Any>
    private lateinit var methodDescriptor: MethodDescriptor<Any, Any>
    private lateinit var callOptions: CallOptions

    companion object {
        val IS_DRY_RUN_METADATA_KEY = Metadata.Key.of("dry-run-key", Metadata.ASCII_STRING_MARSHALLER)
        val IS_DRY_RUN_CALLOPTIONS_KEY = CallOptions.Key.create<Boolean>("dry-run-call-options")
    }

    @BeforeEach
    fun setup() {
        interceptor = MigrateDryRunClientInterceptor()
        mockChannel = mockk()
        mockCall = mockk(relaxed = true)
        methodDescriptor = mockk()
        callOptions = CallOptions.DEFAULT.withOption(IS_DRY_RUN_CALLOPTIONS_KEY, true)

        every { mockChannel.newCall(any(), any()) } returns mockCall
    }

    @Test
    fun `should intercept call and set dry-run metadata`() {
        val interceptedCall = interceptor.interceptCall(methodDescriptor, callOptions, mockChannel)

        // Verify that the new call is made using the correct method and call options
        verify { mockChannel.newCall(methodDescriptor, callOptions) }

        // Mock Metadata and ResponseListener
        val headers = Metadata()
        val responseListener = mockk<ClientCall.Listener<Any>>(relaxed = true)

        interceptedCall.start(responseListener, headers)

        // Validate that the metadata header is set with the correct dry-run value
        assertEquals("true", headers.get(IS_DRY_RUN_METADATA_KEY))

        // Verify that start is called on the original call
        verify { mockCall.start(responseListener, headers) }
    }
}
```

---

### **Explanation of the Test:**
1. **Mocks dependencies**:
   - `Channel`, `ClientCall`, `MethodDescriptor`, `CallOptions`, and `Metadata`.
   
2. **Intercepts a gRPC call**:
   - Ensures `next.newCall` is called with the correct method and options.

3. **Checks `start` behavior**:
   - Ensures `IS_DRY_RUN_METADATA_KEY` is set correctly in `Metadata`.
   - Uses `assertEquals` to verify the expected header value.
   - Verifies that `start` is actually invoked on the forwarded call.

This test ensures your interceptor correctly modifies the metadata before sending the request. Let me know if you need additional refinements!
