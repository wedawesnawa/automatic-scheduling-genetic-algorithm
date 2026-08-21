# Automatic Scheduling Using a Genetic Algorithm

![Preview (GIF)](Video%20Project-1.gif)

## 📖 About

This project was developed as part of a university research assignment to evaluate the effectiveness of the Genetic Algorithm (GA) in solving the university course timetabling problem.

The system automatically generates semester schedules by considering courses, lecturers, classes, and available time slots. Instead of manually arranging schedules, the Genetic Algorithm searches 
for an optimal timetable while minimizing scheduling conflicts and maximizing the fitness value.

## ✨ Features
* Course management
* Lecturer management
* Class management
* Time slot management
* Automatic timetable generation
* Genetic Algorithm optimization
* Fitness score evaluation
* Semester-based scheduling


## 🛠️ Tech Stack
| Category        | Technology           |
| --------------- | -------------------- |
| Language        | Python               |
| Framework       | Streamlit            |
| Algorithm       | Genetic Algorithm    |
| Data Processing | Pandas               |
| Visualization   | Streamlit Components |


## 🚀 Installation
1. git clone `https://github.com/wedawesnawa/automatic-scheduling-genetic-algorithm.git`
2. Create a virtual environment `python -m venv venv`
3. Activate the environment `venv\Scripts\activate`
4. Install dependencies `pip install -r requirements.txt`
5. Run the application `streamlit run main.py`
6. Open `http://localhost:8501`

## 📷 Screenshots

![Image](https://drive.google.com/uc?id=15LI4JjhbAbB1ccX0W9HJKJ5v4IpBY-nA)  
![Image](https://drive.google.com/uc?id=1xhV4L2bNs_VxF7DL6_NmGG_ZNmi4ShSk) 
![Image](https://drive.google.com/uc?id=13NVivhkt_0B7ejiff0bG6SsIWrk040S_)
![Image](https://drive.google.com/uc?id=1PNQOSHX5Ai44MAIRtxmTsgjL2XrhoMsF)
![Image](https://drive.google.com/uc?id=1lwJ7GIqkogUnlVPAhMhJ63M1EdGhLRUQ)
## Folder Structure
![Image](https://drive.google.com/uc?id=1nzQCcKFWiKoK1pq5pC35t9MLJZ9BLe1v)

## 🎯 Challenges
Developing an automatic timetable generator involved several challenges:

* Collecting and validating scheduling data.
* Defining scheduling constraints for lecturers, courses, classrooms, and time slots.
* Designing an appropriate chromosome representation.
* Balancing exploration and exploitation during the optimization process.

## 🔮 Future Improvements
Several improvements can further enhance the system:

* Support soft and hard scheduling constraints separately.
* Improve chromosome representation for better convergence.
* Enhance the fitness function to reduce unscheduled courses.
* Add classroom capacity constraints.
* Support multiple study programs.
* Export schedules to PDF and Excel.
* Compare the Genetic Algorithm with other optimization algorithms such as Particle Swarm Optimization (PSO), Simulated Annealing (SA), or Tabu Search.
* Improve visualization of scheduling conflicts and algorithm statistics.
