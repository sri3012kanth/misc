Here’s how to enhance the email template with **Thymeleaf variables** to make it dynamic. This allows you to use Spring Boot's templating capabilities to populate the template with real data.

---

### **Updated Thymeleaf Template with Variables**

Save this template as `email-template.html` in the `src/main/resources/templates` directory.

```html
<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        .email-container {
            max-width: 600px;
            margin: 20px auto;
            background: #ffffff;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .header {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .intro {
            font-size: 16px;
            color: #555;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        table th, table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        table th {
            background-color: #f2f2f2;
            color: #333;
        }
        .footer {
            font-size: 14px;
            color: #888;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header -->
        <div class="header" th:text="${emailSubject}">Your Report Summary</div>

        <!-- Introductory Text -->
        <div class="intro">
            Dear <span th:text="${userName}">User</span>,<br><br>
            Below is the summary of your recent activities and performance metrics. Please review the details in the tables below.
        </div>

        <!-- First Table -->
        <table>
            <thead>
                <tr>
                    <th>Activity</th>
                    <th>Status</th>
                    <th>Completion Date</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="activity : ${activities}">
                    <td th:text="${activity.activity}">Project A</td>
                    <td th:text="${activity.status}">Completed</td>
                    <td th:text="${activity.date}">2024-12-10</td>
                </tr>
            </tbody>
        </table>

        <!-- Second Table -->
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                <tr th:each="metric : ${metrics}">
                    <td th:text="${metric.metric}">Tasks Completed</td>
                    <td th:text="${metric.value}">45</td>
                </tr>
            </tbody>
        </table>

        <!-- Footer -->
        <div class="footer">
            Thank you,<br>
            The Team
        </div>
    </div>
</body>
</html>
```

---

### **Java Code to Render the Template**

1. **Email Service**:
   Use the following Spring Boot service to send emails:

   ```java
   @Service
   public class EmailService {

       @Autowired
       private JavaMailSender mailSender;

       @Autowired
       private SpringTemplateEngine templateEngine;

       public void sendEmail(String recipient, String subject, Map<String, Object> model) {
           MimeMessage mimeMessage = mailSender.createMimeMessage();

           try {
               MimeMessageHelper helper = new MimeMessageHelper(mimeMessage, true);
               helper.setTo(recipient);
               helper.setSubject(subject);

               // Generate email content from the Thymeleaf template
               Context context = new Context();
               context.setVariables(model);
               String htmlContent = templateEngine.process("email-template", context);

               helper.setText(htmlContent, true);
               mailSender.send(mimeMessage);
           } catch (MessagingException e) {
               e.printStackTrace();
           }
       }
   }
   ```

2. **Populate Variables in the Model**:
   Prepare the model and call the `sendEmail` method:

   ```java
   Map<String, Object> model = new HashMap<>();
   model.put("emailSubject", "Your Report Summary");
   model.put("userName", "John Doe");
   model.put("activities", List.of(
       Map.of("activity", "Project A", "status", "Completed", "date", "2024-12-10"),
       Map.of("activity", "Project B", "status", "In Progress", "date", "N/A")
   ));
   model.put("metrics", List.of(
       Map.of("metric", "Tasks Completed", "value", "45"),
       Map.of("metric", "Pending Tasks", "value", "12")
   ));

   emailService.sendEmail("user@example.com", "Your Report Summary", model);
   ```

---

### **Result**
When the email is rendered and sent:
- The `emailSubject`, `userName`, `activities`, and `metrics` will be dynamically replaced with their corresponding values.
- The tables will display the data provided in the `activities` and `metrics` lists.

---

### **Customization Options**
- You can add more variables or fields in the template.
- Use conditional expressions in Thymeleaf (e.g., `th:if`, `th:unless`) to display optional content dynamically.
- Add inline styles or external CSS for more design customizations.
