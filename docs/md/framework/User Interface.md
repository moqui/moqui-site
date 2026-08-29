#  User Interface

The main artifact for building user interfaces in Moqui Framework is the XML Screen.

XML Screens are designed to be used with multiple render modes using the same screen definition. This includes various types of text output for user and system interfaces, and code-driven user interfaces in client applications.

To accommodate this design goal most screen elements are render mode agnostic. For elements that are specific to a particular render mode there is a render-mode element with subelements designed for specific render modes. To support multiple render mode specific elements in the same screen just put a subelement under the render-mode element for each desired type.

In a web-based application a XML Screen is the main way to produce output for incoming requests. The structure of screens makes it easy to support any sort of URL to a screen.

 In this section we cover the following topics-
 -  XML Screen
 -  XML Form
 -  Templates
 -  Sending and Receiving Email
 

