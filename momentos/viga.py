from anastruct import SystemElements

class ElementosBarra():

    def __init__(self, dados):
        self.dados = dados
        self.nos, self.elementos, _ = self.dados
        
    def set_location(self, nos):
        location = []
        x = []
        elementos = self.dados[self.elementos]
        #print(elementos.values())
        
        for noi, nof in elementos.values():
            xi = self.dados[self.nos][noi]
            xf = self.dados[self.nos][nof]
            x.append(xi)
            x.append(xf)
        for i in x:
            if i not in nos:
                nos.append(i)
        nos = sorted(nos)
        #print(nos)
        for i in range(len(nos) -1):
            xi = nos[i]
            xf = nos[i + 1]
            location.append([[xi, 0], [xf, 0]])
        return location

    def add_elementos(self, viga: SystemElements, nos) -> None:
        for add in self.set_location(nos):
            viga.add_element(location=add)

    def set_nos(self):
        nos = [[i, 0] for i in self.dados[self.nos].values()]
        return nos
    
    def nos_map(self, viga: SystemElements):
        nos_map = [viga.find_node_id(vertex) for vertex in self.set_nos()]
        return nos_map

    @property
    def m(self):
        return self["m"]
    
class ApoiosBarra():

    def __init__(self, dados):
        self.nos, self.apoio = dados["nos"], dados["apoios"]

    
    def add_apoio(self, viga: SystemElements, nos)-> None:
        for name, no_id in nos:#
            if name == "hinged":
                viga.add_support_hinged(no_id)
            
            if name == "roll":
                viga.add_support_roll(no_id)
            
            if name == "fixed":
                viga.add_support_fixed(no_id)

    def nos_apoios(self, viga:SystemElements):
        apoios = []
        for no_id, tipo in self.apoio.items():
            apoios.append([tipo, viga.find_node_id([self.nos[no_id], 0])])
        return apoios
    
    def nos_apoios_iso(self, viga: SystemElements, nos: dict):
        apoios = []
        for no_id, tipo in nos.items():
            apoios.append([tipo, viga.find_node_id([self.nos[no_id], 0])])
        return apoios
    

if __name__ == "__main__":
    est = {
    "nos" : {"1": 0.0, "2": 8.0, "3": 16.0},
    "elementos" : {"1": ["1", "2"], "2" : ["2","3"]},
    "apoios" : {"1": "hinged", "2" : "roll", "3" : "roll"}}

    ele = ElementosBarra(est)
    print(ele.set_location([1,2,3, 4, 10,11,12]))