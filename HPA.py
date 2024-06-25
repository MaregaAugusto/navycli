from kubernetes import client
import ruamel.yaml as Yaml
#from ruamel.yaml import YAML

class HPA:

    def __init__(self, namespace):
        self.namespace = namespace
        self.autoscaling_v1 = client.AutoscalingV1Api()
        try:
            response = self.autoscaling_v1.list_namespaced_horizontal_pod_autoscaler(namespace=self.namespace)
            # Get the list of HPA from the response
            self.hpas = response.items
        except Exception as e:
            print(f"Error listing HPA: {e}")
    
    def __str__(self):
        for hpa in self.hpas:
            print(f"HPA Name: {hpa.metadata.name}")
            print(f"Min Replicas: {hpa.spec.min_replicas}")
            print(f"Max Replicas: {hpa.spec.max_replicas}")
        print("-------------------")
    ######################################################################################################################
    def update_hpa_max(self, hpa, new_max_replicas):
        # Verificar si el nuevo maximo es diferente del actual
        if new_max_replicas != hpa.spec.max_replicas:
            # Actualizar el valor Maximo en el objeto HPA
            hpa.spec.max_replicas = new_max_replicas

            # Actualizar el HPA en el servidor de Kubernetes
            try:
                self.autoscaling_v1.replace_namespaced_horizontal_pod_autoscaler(body=hpa, name=hpa.metadata.name, namespace=self.namespace)
                print(f"Actualizar: {hpa.metadata.name} Maximo: {new_max_replicas}")
                print("-------------------")
            except Exception as e:
                print(f"Error al actualizar HPA '{hpa.metadata.name}': {e}")
    
    def update_hpa_min(self, hpa, new_min_replicas):
        # Verificar si el nuevo mínimo es diferente del actual
        if new_min_replicas != hpa.spec.min_replicas:
            # Actualizar el valor mínimo en el objeto HPA
            hpa.spec.min_replicas = new_min_replicas

            # Actualizar el HPA en el servidor de Kubernetes
            try:
                self.autoscaling_v1.replace_namespaced_horizontal_pod_autoscaler(body=hpa, name=hpa.metadata.name, namespace=self.namespace)
                print(f"Actualizar: {hpa.metadata.name}  Mínimo: {new_min_replicas}")
                print("-------------------")
            except Exception as e:
                print(f"Error al actualizar HPA '{hpa.metadata.name}': {e}")
       
    ####################################################################################################################################
    def max_replica_iteractivo(self):
        for hpa in self.hpas:
            print(f"HPA Name: {hpa.metadata.name}")
            print(f"Min Replicas: {hpa.spec.min_replicas}")
            print(f"Max Replicas: {hpa.spec.max_replicas}")
            user_input = input("ingrese número pods de maxima necesarios o enter para continuar: ")
            if user_input:
                new_max_replicas = int(user_input)
            else:
                new_max_replicas = hpa.spec.max_replicas

            self.update_hpa_max(hpa, new_max_replicas)
            print("-------------------")
        
    def min_replica_iteractivo(self):
        for hpa in self.hpas:
            print(f"HPA Name: {hpa.metadata.name}")
            print(f"Min Replicas: {hpa.spec.min_replicas}")
            print(f"Max Replicas: {hpa.spec.max_replicas}")
            user_input = input("ingrese número pods de minimo necesarios o enter para continuar: ")
            if user_input:
                new_min_replicas = int(user_input)
            else:
                new_min_replicas = hpa.spec.min_replicas

            self.update_hpa_min(hpa, new_min_replicas)
            print("-------------------")

    def max_replica_file(self, path):
        yaml= Yaml.YAML(typ='safe')
        with open(path , 'r') as file:
            data = yaml.load(file)
            for hpa in self.hpas:
                new_max_replicas = data[hpa.metadata.name]["max_replicas"]
                self.update_hpa_max(hpa, new_max_replicas)

    def min_replica_file(self, path):
        yaml= Yaml.YAML(typ='safe')
        with open(path , 'r') as file:
            data = yaml.load(file)
            for hpa in self.hpas:
                new_min_replicas = data[hpa.metadata.name]["min_replicas"]
                self.update_hpa_min(hpa, new_min_replicas)

    def createFileHpa(self, path):
        datos = {}
        for hpa in self.hpas:
            datos[hpa.metadata.name] = { 
                "min_replicas" : hpa.spec.min_replicas,
                "max_replicas" : hpa.spec.max_replicas
                }

        yaml = Yaml.YAML(typ='safe', pure=True)
        yaml.default_flow_style = False
        with open(path , "w") as archivo:
            yaml.dump(datos, archivo)

        print("Datos guardados en archivo hpas.yaml")

