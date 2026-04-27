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
## ✨ Core Features

**Multi-Layered Network Generation**: Simulates formal corporate hierarchies and departmental clusters

**Agent Logic**:

- **Everett Rogers Categories**: Agents are assigned as Innovators, Early Adopters, Early Majority, Late Majority, or Laggards based on statistical probabilities.

- **Age & Seniority Decoupling**: Age and seniority are correlated but distinct. Older agents have naturally higher resistance to change.

**Organizational Culture (Quinn-Cameron CVF)**: Define the global environment to manipulate network density and peer influence:

- 🤝 **Clan**: High peer influence, dense informal networks.

- 🚀 **Adhocracy**: Low adoption thresholds, high innovator generation.

- ⚔️ **Market**: Siloed departments, competitive adoption triggers.

- 🏛️ **Hierarchy**: Strict top-down influence, high resistance.

**Threshold-Based Adoption**: Agents dynamically calculate adoption based on their innate resistance and the ratio of connected peers who have already adopted.

## 🛠️ Tech Stack

Language: Python 3.9+

Graph & Network Theory: NetworkX

Data Manipulation: Pandas, NumPy

Visualization: Matplotlib

## 🚧 WIP 🚧
