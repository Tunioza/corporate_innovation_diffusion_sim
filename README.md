# 🏢 Corporate Innovation Diffusion Simulator

> **You know that feeling when leadership spends a fortune on a modern tech stack like Power BI or Tableau Desktop, but six months later, half the company is still manually updating the same broken Excel spreadsheet? That friction is exactly why I'm building this project. I dont want to just ask why it happens, I want to see what causes it in detail**

This project is based around idea of Agent-Based Simulation (ABS) built in Python to model how new technologies, software stacks, and workflows diffuse through a company's workforce.

This project bridges Network Theory and Organizational Behavior by simulating a corporate network where employees are distinct agents. It answers critical business questions about change management by modeling Everett Rogers' Diffusion of Innovations, Quinn-Cameron's Corporate Culture framework, and realistic demographic behaviors.
## 📖 Project Overview

When a company introduces a new tool, adoption is rarely instantaneous. Sometimes it spreads like wildfire, other times, a stubborn senior manager blocks it completely. This simulation models these complex, emergent dynamics to test deployment strategies:

1. How fast will an innovation spread naturally?

2. How seniority of employees impact diffusion of innovation?
   
3. How do different corporate cultures impact the flow of new ideas?

By tweaking the parameters of the environment, users can run experiments to find the optimal strategy for deploying new technologies in different organizational structures.

## 👥 The Agents

The **Agents** in this simulation represent **individual employees** within a corporate network. Each agent possesses unique psychological and professional traits that dictate their behavior:

**1. Psychological Profile (Rogers' Categories)**

Each agent is assigned a persona based on statistical probabilities:
* **Innovators & Early Adopters**: Low resistance, they seek out change.
* **Early & Late Majority**: Threshold-driven, they wait for social proof.
* **Laggards**: High resistance, they are the last to adopt.

**2. Demographic Attributes**

* **Age vs. Seniority**: These are correlated but distinct. While seniority increases an agent's influence, older agents have naturally higher resistance to change.
* **Departmental Affiliation**: Defines which silos the agent belongs to in the organizational network.

**3. Decision Logic (The Threshold)**

Agents calculate adoption based on **Threshold-Based Logic**. They transition from "Non-Adopter" to "Adopter" only when the combined influence of their connected peers who have adopted outweighs their innate resistance.

## 🌐 Environment: Network Topology

The simulation environment will be constructed using `NetworkX` to represent the social and professional structure of the organization. The choice of network graph is still in consideration. Two primary ideas are:

**1. Barabási–Albert (Scale-Free) Model**
   
This model simulates a "Power Law" distribution where a few agents have a vast number of connections, while most have very few.
* **Corporate Context**: Represents organizations dominated by "Super-Connectors" or high-profile leaders who influence many people simultaneously.
* **Diffusion Impact**: Innovations spread rapidly if they hit a hub, but can be easily contained if hubs are resistant.

**2. Watts–Strogatz (Small-World) Model**
   
This model creates a network with high clustering and short path lengths.
* **Corporate Context**: Perfectly mirrors departmental silos where "everyone knows everyone" within a team, but "bridge agents" are required to pass information to other departments.
* **Diffusion Impact**: Captures the "echo chamber" effect, where adoption happens in localized bursts before jumping across the organization.

## ✨ Core Features


**Multi-Layered Network Generation**: Simulates formal corporate hierarchies and departmental clusters

**Agent Logic**:

- **Everett Rogers Categories**: Agents are assigned as Innovators, Early Adopters, Early Majority, Late Majority, or Laggards based on statistical probabilities.

- **Age & Seniority Decoupling**: Age and seniority are correlated but distinct. Older agents have naturally higher resistance to change.

**Organizational Culture (Quinn-Cameron CVF)**: Define the global environment to manipulate network density and peer influence:


<p align="center">
<img align="center" width="476" height="416" alt="afb-2-1" src="https://github.com/user-attachments/assets/6d0b69dd-67a4-4ab0-ac15-e3527e866eca" />
</p>


- 🤝 **Clan**: High peer influence, dense informal networks.

- 🚀 **Adhocracy**: Low adoption thresholds, high innovator generation.

- ⚔️ **Market**: Siloed departments, competitive adoption triggers.

- 🏛️ **Hierarchy**: Strict top-down influence, high resistance.

**Threshold-Based Adoption**: Agents dynamically calculate adoption based on their innate resistance and the ratio of connected peers who have already adopted.

## 🔀 Flowchart

<img width="1920" height="1080" alt="Initialize Network Topology" src="https://github.com/user-attachments/assets/53e21e5a-6bde-44a6-ae39-bac604ab649a" />

## 🛠️ Tech Stack

Language: Python 3.9+

Graph & Network Theory: NetworkX

Data Manipulation: Pandas, NumPy

Visualization: Matplotlib

## 🚧 WIP 🚧
