# Moqui: A Secure, Scalable Framework for Building Powerful Applications
Moqui empowers businesses to build robust and secure applications with confidence. This document highlights Moqui's strengths in three key areas: Security, Scalability, and Community Support.
[TOC levels=2-3]

## Unwavering Security
Moqui prioritizes the protection of your sensitive data. A comprehensive suite of security features ensures your application remains a fortress:
* **Authentication and Authorization:**
  * **Session Management:** Control session duration to mitigate unauthorized access risks. Moqui allows you to define session timeouts, preventing sessions from staying active for extended periods if a user forgets to log out.
  * **Password Security:** Enforce strong password policies with configurable settings like minimum length, history, and expiry. You can define complexity requirements to ensure users create passwords that are resistant to cracking. Additionally, Moqui can enforce password rotation to prevent attackers from leveraging compromised credentials for extended periods.
  * **API Access Management:** Secure API access with token-based authentication.
* **Data Encryption:** Implement robust data encryption protocols to safeguard data at rest and in transit. Moqui supports integration with encryption technologies to protect sensitive data stored in your database and during transmission between the client and server.
* **Network Security:** 
  * **Firewall Tools:** You can use tools like iptables or ufw to enhance network protection. Moqui can leverage these firewall tools to restrict incoming and outgoing traffic based on predefined rules, further securing your application.
  * **Rate Limiting:**  An artifact tarpit limits the velocity of access to artifacts in a group. When a particular user exceeds the configured velocity limit for a particular artifact or a particular type the framework creates an ArtifactTarpitLock record to restrict access to that artifact by the user until a certain date/time. All of this is configurable.
Also, you can prevent brute-force attacks through rate limiting mechanisms within firewall settings or load balancers. Moqui can be configured to limit login attempts or API requests from a single source, making it more difficult for attackers to automate unauthorized access attempts.
* **Secure Development Practices:**
  * **Docker Security:** Manage Docker configurations securely, including controlling open ports in development and production environments. By following secure containerization practices, you can minimize the attack surface of your Moqui application.
  * **Credential Storage:** Utilize best practices for storing credentials securely (e.g., environment variables). Moqui discourages storing sensitive information directly in code and instead promotes the use of environment variables or secure configuration files to manage credentials.

## Effortless Scalability
Moqui applications seamlessly adapt to accommodate your growing business needs. Leverage vertical and horizontal scaling techniques to handle ever-increasing demands:
* **Vertical Scaling:** Scale up processing power and memory on your existing server for a straightforward solution to initial load spikes.
* **Horizontal Scaling:** Distribute workloads across multiple servers for:
  * **Application Server:** Utilize Hazelcast and a load balancer for horizontal scaling of the application server. Hazelcast is a distributed in-memory data grid that can improve performance and scalability by caching frequently accessed data across multiple servers. A load balancer can then distribute incoming requests across these application servers, ensuring optimal resource utilization.
  * **Database:** Moqui is a DB agnostic framework and can connect to the DB of your choice. You can Implement read replicas to complement your primary database (e.g., MySQL or PostgreSQL). Read replicas share the read-only copy of your database, allowing you to distribute read queries and improve overall database performance.
  * **Open Search:** Leverage sharding techniques for horizontal scaling of Open Search, the search and analytics engine. Open Search can be horizontally scaled by distributing data shards across multiple servers. This improves query performance and allows you to handle increasing data volumes. 
* **Performance Benchmarks:** Consider providing reference data showcasing real-world Moqui deployments:
  * **Success Stories:** [TODO] Case studies of businesses that have successfully scaled Moqui applications. These stories provide valuable insights into how other organizations have achieved scalability with Moqui.
  * **Load Testing Resources:** [TODO] Offer downloadable load testing scripts (e.g., JMeter scripts) to help businesses evaluate Moqui's performance under various load conditions on their specific hardware. This allows businesses to consider Moqui with more confidence after conducting their own performance assessments.

## Thriving Community
Moqui is backed by a passionate and supportive community of developers and users. This community fosters a collaborative environment where you can find valuable resources and connect with experts:
* **Active Forum:** Engage in discussions on the Moqui Forum, a treasure trove of knowledge and support. Get help, share insights, and stay up-to-date on the latest Moqui developments. (Consider adding information about the calendar being added to the website for community meetings)
* **Success Stories:** Discover the potential of Moqui by exploring real-world success stories. Learn how other businesses have leveraged Moqui to build powerful and scalable applications.
 
## Build with Confidence
Moqui empowers you to build secure, scalable applications with confidence. Explore Moqui's capabilities and join the thriving community to unlock the potential.

 

  
