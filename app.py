from flask import Flask, request, jsonify
from models.task import *
app = Flask(__name__)

tasks = []

task_id = 1

@app.route("/tasks", methods=["POST"])
def create_task():

    global task_id
    data = request.get_json()
    new_task = Task(id=task_id, tittle=data["tittle"], description=data.get("description", "")) 
    task_id += 1
    tasks.append(new_task)

    for task in tasks:
        print(task.id, task.tittle, task.description)

    return jsonify({"message": "Nova tarefa criada com sucesso"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    task_list = []

    for task in tasks:
        task_list.append(task.to_dict())

    output = {
                "tasks":
                    {
                    "tittle": task_list,
                    "total_tasks": len(task_list)
                    }             
            }
    
    return jsonify(output)  

@app.route("/tasks/<int:id>", methods=["GET"]) 
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
        
    return jsonify({"message": "Não foi possível encontrar a tarefa"}), 404

@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.get_json()

    for task in tasks:
        if task.id == id:
            task.tittle = data.get("tittle", task.tittle)
            task.description = data.get("description", task.description)
            task.completed = data.get("completed", task.completed)
            return jsonify({"message": "Tarefa atualizada com sucesso"})
        
    return jsonify({"message": "Não foi possível encontrar a tarefa"}), 404

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = None

    for t in tasks:
        if t.id == id:
            task = t 
            break

    if not task:
        return jsonify({"message": "Não foi possível encontrar a tarefa"}), 404
    
    tasks.remove(task)
    return jsonify({"message": "Tarefa deletada com sucesso"})

if __name__ == "__main__":
    app.run(debug=True)
