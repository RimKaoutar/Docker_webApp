from flask import Flask, render_template, request, redirect, url_for
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def index():
    containers = client.containers.list(all=True)
    images = [image.tags[0] for image in client.images.list()]
    return render_template('index.html', containers=containers, images=images)

@app.route('/start/<id>')
def start_container(id):
    container = client.containers.get(id)
    container.start()
    return redirect(url_for('index'))

@app.route('/stop/<id>')
def stop_container(id):
    container = client.containers.get(id)
    container.stop()
    return redirect(url_for('index'))

@app.route('/pause/<id>')
def pause_container(id):
    container = client.containers.get(id)
    container.pause()
    return redirect(url_for('index'))

@app.route('/unpause/<id>')
def unpause_container(id):
    container = client.containers.get(id)
    container.unpause()
    return redirect(url_for('index'))

@app.route('/create', methods=['POST'])
def create_container():
    image = request.form['image']
    name = request.form['name']
    
    
    container = client.containers.create(
        image=image,
        name=name,
        stdin_open=True,
        tty=True,
        command=None,
        detach=True
    )
    container.start()
    return redirect(url_for('index'))



@app.route('/delete/<id>')
def delete_container(id):
    container = client.containers.get(id)
    container.stop()
    container.remove()
    return redirect(url_for('index'))

@app.route('/all/start')
def start_all_containers():
    containers = client.containers.list(all=True)
    for container in containers:
    	if container.status == 'exited':
        	container.start()
    return redirect(url_for('index'))

@app.route('/all/stop')
def stop_all_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        if container.status == 'paused':
	        container.unpause()
	        container.stop()
        if container.status == 'running':	
            container.stop()
    return redirect(url_for('index'))

@app.route('/all/pause')
def pause_all_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        if container.status == 'running':
            container.pause()
    return redirect(url_for('index'))

@app.route('/all/unpause')
def unpause_all_containers():
    containers = client.containers.list(all=True)
    for container in containers:
    	if container.status == 'paused':
	        container.unpause()
    return redirect(url_for('index'))

@app.route('/all/delete')
def delete_all_containers():
    containers = client.containers.list(all=True)
    for container in containers:
        container_status = container.status
        if container_status == 'running' or container_status == 'paused':
            try:
                container.stop()
            except docker.errors.APIError:
                pass
        container.remove(force=True)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

