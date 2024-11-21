To define multiple event schemas for the `data` section in an OpenAPI specification, you can leverage the `oneOf` or `anyOf` constructs. This allows you to specify that the `data` section of the CloudEvent can conform to one of several predefined schemas, depending on the type of event.

Here’s how you can do it:

---

### 1. **Define Common CloudEvent Attributes**
Create a reusable schema for the general CloudEvent structure and use `oneOf` to specify multiple possible schemas for the `data` field.

#### Example:
```yaml
components:
  schemas:
    CloudEvent:
      type: object
      required:
        - specversion
        - id
        - source
        - type
        - data
      properties:
        specversion:
          type: string
          description: Version of the CloudEvents specification.
          example: "1.0"
        id:
          type: string
          description: Unique identifier for the event.
          example: "abc123"
        source:
          type: string
          description: Source of the event.
          example: "/myapp/resource"
        type:
          type: string
          description: Type of the event.
          example: "com.example.user.created"
        time:
          type: string
          format: date-time
          description: Timestamp of the event.
          example: "2024-11-21T10:30:00Z"
        data:
          oneOf:
            - $ref: '#/components/schemas/UserCreatedEvent'
            - $ref: '#/components/schemas/UserUpdatedEvent'
            - $ref: '#/components/schemas/OrderCreatedEvent'
          description: Event payload specific to the event type.

    UserCreatedEvent:
      type: object
      properties:
        userId:
          type: string
          description: Unique ID of the user.
          example: "user-789"
        userName:
          type: string
          description: Name of the user.
          example: "John Doe"
        email:
          type: string
          format: email
          description: Email address of the user.
          example: "johndoe@example.com"
      required:
        - userId
        - userName

    UserUpdatedEvent:
      type: object
      properties:
        userId:
          type: string
          description: Unique ID of the user.
          example: "user-789"
        updatedFields:
          type: array
          items:
            type: string
          description: List of fields that were updated.
          example: ["email", "phone"]
      required:
        - userId
        - updatedFields

    OrderCreatedEvent:
      type: object
      properties:
        orderId:
          type: string
          description: Unique ID of the order.
          example: "order-456"
        orderTotal:
          type: number
          format: float
          description: Total amount for the order.
          example: 123.45
        items:
          type: array
          items:
            type: object
            properties:
              itemId:
                type: string
                description: Unique ID of the item.
                example: "item-123"
              quantity:
                type: integer
                description: Quantity of the item.
                example: 2
      required:
        - orderId
        - orderTotal
```

---

### 2. **Customize the `type` Field to Match `data`**
   - Define the `type` field to correlate with the specific schema in the `data` field.
   - Provide examples for clarity.

#### Example Mapping Table:
| `type` Value                  | `data` Schema              |
|-------------------------------|----------------------------|
| `com.example.user.created`    | `UserCreatedEvent`         |
| `com.example.user.updated`    | `UserUpdatedEvent`         |
| `com.example.order.created`   | `OrderCreatedEvent`        |

---

### 3. **Add Examples**
Provide examples for different event types to make it easier for consumers to understand.

#### Example:
```yaml
examples:
  UserCreatedEventExample:
    summary: Example of a User Created Event
    value:
      specversion: "1.0"
      id: "user-event-1"
      source: "/myapp/users"
      type: "com.example.user.created"
      time: "2024-11-21T12:00:00Z"
      data:
        userId: "user-123"
        userName: "John Doe"
        email: "johndoe@example.com"

  OrderCreatedEventExample:
    summary: Example of an Order Created Event
    value:
      specversion: "1.0"
      id: "order-event-1"
      source: "/myapp/orders"
      type: "com.example.order.created"
      time: "2024-11-21T14:00:00Z"
      data:
        orderId: "order-456"
        orderTotal: 250.75
        items:
          - itemId: "item-789"
            quantity: 1
          - itemId: "item-456"
            quantity: 2
```

---

### 4. **Share the Specification**
- Export the OpenAPI file in YAML or JSON format.
- Provide clients with this file along with a description of the `type` values and their corresponding `data` schemas.
- Use tools like Swagger UI or Redoc for easy visualization.

---

Would you like help generating this schema dynamically or converting it to AsyncAPI for better event-driven system compatibility?
