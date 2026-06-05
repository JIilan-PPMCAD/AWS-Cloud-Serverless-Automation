# AWS Serverless Architecture & Cloud Automation

This repository contains a comprehensive suite of cloud automation solutions developed using **AWS Lambda** and the **Boto3 SDK** for Python. These projects demonstrate how to automate routine infrastructure tasks, enhance security, and optimize costs in an AWS environment.

---

## 📂 Project Structure

Each assignment is contained within its own directory, including the Python source code, a dedicated README, and a `screenshots/` folder containing proof of execution.


| Assignment | Task Title | Status |
| :--- | :--- | :--- |
| **[Assignment 01](./Assignment_01_EC2_Management/)** | **Automated EC2 Instance Management** | ✅ Completed |
| **[Assignment 02](./Assignment_02_S3_Cleanup/)** | **Automated S3 Bucket Cleanup** | ✅ Completed |
| **[Assignment 03](./Assignment_03_S3_Security/)** | **Monitor Unencrypted S3 Buckets** | ✅ Completed |
| **[Assignment 04](./Assignment_04_EBS_Snapshots/)** | **Automatic EBS Snapshot and Cleanup** | ✅ Completed |
| **[Assignment 05](./Assignment_05_EC2_Auto_Tagging/)** | **Auto-Tagging EC2 Instances on Launch** | ✅ Completed |

---

## 🚀 Assignments Summary

### 1. Automated EC2 Instance Management
Developed a Lambda function that identifies EC2 instances with specific tags (`Auto-Stop` and `Auto-Start`) and manages their power state accordingly. This helps in reducing costs by ensuring non-production instances are only running when needed.

### 2. Automated S3 Bucket Cleanup
(Planned) A script to scan S3 buckets and delete objects older than a specified threshold (e.g., 30 days) to prevent storage bloat.

### 3. Monitor Unencrypted S3 Buckets
(Planned) A security-focused automation that audits S3 buckets and reports or remediates buckets found without Server-Side Encryption (SSE).

### 4. Automatic EBS Snapshot and Cleanup
(Planned) Automating the backup of EBS volumes via snapshots and implementing a retention policy to delete older snapshots to manage costs.

### 5. Auto-Tagging EC2 Instances on Launch
(Planned) Integrating EventBridge with Lambda to automatically apply standardized tags to new EC2 instances as soon as they are launched.

---

## 🛠️ Tools & Technologies
*   **Language:** Python 3.x
*   **SDK:** Boto3
*   **Services:** AWS Lambda, EC2, S3, IAM, CloudWatch, EventBridge
*   **Version Control:** Git & GitHub

## 🎓 Program
**Postgraduate Program in Multi Cloud Architecture & Cloud Automation**
