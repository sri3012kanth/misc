Here’s a complete Markdown (`.md`) file sample for a **Pull Request (PR) template** tailored for an Azure Function project:

```markdown
# Pull Request Template

## **Pull Request Title**
<!-- Provide a descriptive title for this PR -->
`<Feature/bug/task description>`

---

## **Description**
<!-- A concise summary of the changes in this PR -->
- **What does this PR do?**  
  - `<Explain what is being added, updated, or fixed>`  
- **Why are these changes needed?**  
  - `<Explain the reasoning behind the changes>`  

---

## **Checklist**
Please ensure that the following requirements are met before submitting the PR:

- [ ] Code builds successfully without errors.
- [ ] Unit tests cover the new or updated functionality.
- [ ] Unit tests and integration tests pass successfully.
- [ ] All code changes are documented with comments or inline documentation.
- [ ] Logging and exception handling are implemented appropriately.
- [ ] Code adheres to the [team's coding standards](<link_to_coding_standards>).

---

## **Related Work Items**
<!-- Link Azure DevOps work items or GitHub issues -->
- **Work Items:**  
  - `<Link to Azure DevOps Work Item>`  
- **Bugs/Issues:**  
  - `<Link to Azure DevOps Bug/Issue>`  

---

## **Testing Details**
<!-- Provide information on how the changes were tested -->
- **Test Scenarios:**  
  - `<Describe scenario 1>`  
  - `<Describe scenario 2>`  
  - `<Describe any edge cases>`  
- **Evidence of Testing:**  
  - Attach screenshots or provide test results/logs where applicable.  

---

## **Impact Analysis**
<!-- Provide details of the potential impact -->
- Are there any dependencies on other systems/modules?  
  - `<Yes/No>`  
- What are the potential risks?  
  - `<Describe risks>`  

---

## **Deployment Notes**
<!-- Highlight any changes needed for deployment -->
- **Azure Resource Updates:**  
  - [ ] No changes.  
  - [ ] Configuration updates: `<Describe changes>`  
  - [ ] New Function App settings: `<Describe changes>`  

- **Pipeline Updates:**  
  - [ ] No changes.  
  - [ ] Updated pipelines: `<Describe changes>`  

---

## **Screenshots**
<!-- Attach screenshots if applicable -->
- `<Add any relevant images/logs here>`  

---

## **Additional Notes**
<!-- Include any other relevant information -->
- `<Add additional context for the reviewers here>`  

---

## **Reviewers**
<!-- Assign appropriate reviewers -->
- @Reviewer1  
- @Reviewer2  
- @Reviewer3  

---

Thank you for your contribution! 🎉
```

### **Usage**
- Save this file as `PULL_REQUEST_TEMPLATE.md` in the root of your `.azuredevops` or `.github` folder, depending on your repository type.
- This template will automatically populate the PR description for all new PRs in your repository.
