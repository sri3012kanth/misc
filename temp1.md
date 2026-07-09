# UI Mockup Request – Embedded Template Designer

## Goal

Design a new screen inside our React application that functions like a lightweight Figma or Retool-style page builder.

This is **NOT** for implementation yet. I only want a high-fidelity UI mockup showing how the screen should look and behave.

---

## Objective

Allow business users to visually build dynamic questionnaire templates using our existing React components.

The designer should let users:

* Drag existing components from a component library.
* Arrange them on a design canvas.
* Configure their properties.
* Save the layout as a reusable template.
* Later, the saved template will be rendered on another React page using the same components.

The editor should feel similar to Figma, Retool, or Power Apps, but limited to our own design system and components.

---

## Main Layout

Design a three-column interface.

### Left Panel – Component Library

Organize components into categories.

Example categories:

* Layout

  * Section
  * Row
  * Column
  * Card
  * Divider

* Questionnaire

  * Questionnaire
  * Question Group
  * Question
  * Repeating Section

* Input Controls

  * Text Input
  * Text Area
  * Dropdown
  * Checkbox
  * Radio Group
  * Date Picker
  * Time Picker
  * Number
  * Currency
  * Email

* Existing Business Components

  * Patient Card
  * Address
  * Insurance
  * Diagnosis
  * Provider
  * Appointment

Every item should look draggable.

---

### Center Panel – Design Canvas

This is the largest area.

It should display a visual representation of the page being designed.

Users should be able to:

* Drag components onto the canvas.
* Rearrange components.
* Create sections.
* Create nested layouts.
* Add questionnaire groups.
* Select components.
* See hover and selection outlines.
* Preview spacing.
* View responsive layout guides.

Show a sample questionnaire already placed on the canvas.

Example:

Patient Information

First Name

Last Name

Date of Birth

Gender

Insurance

Insurance Company

Policy Number

---

### Right Panel – Properties

When a component is selected, display editable properties.

Example for a Text Input:

* Label
* Placeholder
* Field Name
* Required
* Width
* Validation
* Help Text
* Default Value

Example for a Questionnaire Section:

* Title
* Description
* Collapsible
* Repeatable
* Number of Columns

---

## Toolbar

At the top include:

* Save Template
* Preview
* Undo
* Redo
* Zoom
* Device Preview
* Search Components

---

## Additional Features

Visually represent:

* Drag-and-drop interactions
* Drop zones
* Resize handles
* Alignment guides
* Empty state for new templates
* Breadcrumb navigation
* Template name
* Status indicator

---

## Visual Style

Create a clean enterprise SaaS interface.

Use inspiration from:

* Figma
* Retool
* Microsoft Power Apps
* Atlassian
* Material Design 3

The UI should look modern, spacious, and professional.

---

## Important

Do NOT implement functionality.

Do NOT generate production React code.

Only create a high-fidelity mockup showing the complete screen and user experience.

Think like a Senior Product Designer creating the first design proposal for stakeholder review.
