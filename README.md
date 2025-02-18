# Heuristics and Optimization

## 📌 Project Overview
This project focuses on solving **optimization problems** using **heuristic approaches**, including **Constraint Satisfaction Problems (CSP)** and **A* search algorithm**. The project is divided into different parts, handling parking allocation and transport optimization.

## 🚀 Getting Started

### 📋 Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required dependencies (install via `requirements.txt` if available)
- A solver for mathematical models (e.g., GLPK, Gurobi)

### 🔧 Installation
Clone the repository:
```sh
git clone https://github.com/your_username/Heuristics-and-Optimization.git
cd Heuristics-and-Optimization
```

## 🏗 Project Structure
```
Heuristics-and-Optimization/
│── 100432070-100432094.pdf   # Project documentation
│── autores.txt               # Authors and contributors
│── Proyecto 2/               # Main project directory
│    ├── parte-1/             # CSP-based optimization
│    │   ├── CSP-calls.sh     # Script for running CSP
│    │   ├── CSPParking.py    # Constraint Satisfaction Problem solver
│    │   ├── CSP-tests/       # Test cases for parking allocation
│    │   │   ├── parking01
│    │   │   ├── parking01.csv
│    │   │   ├── ...
│    ├── parte-2/             # A* search optimization
│    │   ├── ASTAR-calls.sh   # Script for running A*
│    │   ├── ASTARTraslados.py # Pathfinding solver using A*
│    │   ├── ASTAR-tests/     # Test cases for transport optimization
│    │   │   ├── mapa02.txt
│    │   │   ├── mapa03.txt
│    ├── parte-1/part-1.ods   # Data and results for part-1
│    ├── parte-2/data.dat     # Data for mathematical model
│    ├── parte-2/model.mod    # Mathematical model for optimization
```

## 🎯 Usage

### Running the CSP Solver
To execute the Constraint Satisfaction Problem solver:
```sh
python Proyecto 2/parte-1/CSPParking.py
```

### Running the A* Search Solver
To run the A* pathfinding algorithm:
```sh
python Proyecto 2/parte-2/ASTARTraslados.py
```

## ✅ Testing
Test cases are available in:
- `Proyecto 2/parte-1/CSP-tests/`
- `Proyecto 2/parte-2/ASTAR-tests/`

## 🛠 Built With
- **Python 3**
- **A* Algorithm**
- **Constraint Satisfaction Problems (CSP)**
- **Mathematical Optimization (GLPK, Gurobi, etc.)**

## 🤝 Contributing
Feel free to fork the repository, make improvements, and submit a pull request.

---

