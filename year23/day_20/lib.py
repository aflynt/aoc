from queue import Queue

class Module:
    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs
        self.lo_pulses = 0
        self.hi_pulses = 0

    def __str__(self) -> str:
        return f"{self.name}"
    def __repr__(self) -> str:
        return f"Module('{self.name}',{self.inputs},{self.outputs})"
    def get_state_list(self) -> list[int]:
        return []

    def handle_pulse(self, pulse, fm):
        return []
    def get_type(self):
        return "std"

class Flip_flop(Module):
    def __init__(self, name, inputs, outputs):
        super().__init__(name, inputs, outputs)
        self.is_on = False
    def __str__(self) -> str:
        isonchar = "1" if self.is_on else "0"
        return f"%{self.name}: {isonchar}"
    def __repr__(self) -> str:
        return f"Flip_flop('{self.name}',{self.inputs},{self.outputs})"
    def get_type(self):
        return "std"
    def get_state_list(self):
        return [1 if self.is_on else 0]

    def handle_pulse(self, pulse, fm):
        if pulse == 1:
            return []
        elif pulse == 0:
            # flip
            if   self.is_on == True:
                ps = [(0, o, self.name) for o in self.outputs]
                self.is_on = not self.is_on
            elif self.is_on == False:
                self.is_on = not self.is_on
                ps = [(1, o, self.name) for o in self.outputs]
            else:
                assert False
        return ps

class Con(Module):
    def __init__(self,name,  inputs, outputs):
        super().__init__(name, inputs, outputs)
        self.last_pulses = {}
        for iname in inputs:
            self.last_pulses[iname] = 0
    def __str__(self) -> str:
        return f"&{self.name}: {list(self.last_pulses.values())}"
    def __repr__(self) -> str:
        return f"Con('{self.name}',{self.inputs},{self.outputs})"
    def get_state_list(self):
        return list(self.last_pulses.values())

    def handle_pulse(self, pulse, fm):
        self.last_pulses[fm] = pulse

        pulse_vals = self.last_pulses.values()
        output_pulse = 0 if all(pulse_vals) else 1

        pulses = []
        for o in self.outputs:
            p = (output_pulse, o, self.name)
            pulses.append(p)
        return pulses

class Bcaster(Module):
    def __init__(self, name, inputs, outputs):
        super().__init__(name, inputs, outputs)
    def __repr__(self) -> str:
        return f"Bcaster('{self.name}',{self.inputs},{self.outputs})"
    def handle_pulse(self, pulse, fm):
        pulses = []
        for o in self.outputs:
            p = (pulse, o, self.name)
            pulses.append(p)
        return pulses
    def get_state_list(self):
        return []

class Button(Module):
    def __init__(self, name, inputs, outputs):
        super().__init__(name, inputs, outputs)
    def press(self) -> list[tuple[int, str]]:
        #print(f"pressed button")
        pulses = []
        for o in self.outputs:
            pulse = (0, o, self.name)
            pulses.append(pulse)
        return pulses
    def get_state_list(self):
        return []
        
    def __repr__(self) -> str:
        return f"Button('{self.name}',{self.inputs},{self.outputs})"

class Output(Module):
    def __init__(self, name, inputs, outputs):
        super().__init__(name, inputs, outputs)
    def __repr__(self) -> str:
        return f"Output('{self.name}',{self.inputs},{self.outputs})"
    def handle_pulse(self, pulse, fm):
        return []
    def get_state_list(self):
        return []

def get_modules(ms: list[str]) -> dict[str, Module]:

    ms.insert(0, "button -> broadcaster")

    add_output = False
    for m in ms:
        if "output" in m:
            add_output = True

    #print(f"add_output?: {add_output}")

    # module dict of dict_name -> outputs
    mod_dict_outputs = {}
    mod_dict_inputs = {}
    mod_dict_types = {}

    if add_output:
        mod_dict_inputs["output"] = []
        mod_dict_outputs["output"] = []
        mod_dict_types["output"] = "output"
    
    for m in ms:
        ty,output = m.split(" -> ")
        name = ty.removeprefix("%").removeprefix("&")
        os = output.split(", ")
    
        if   ty[0] == "%": tyname = "flip-flop"
        elif ty[0] == "&": tyname = "con"
        elif name  == "broadcaster": tyname = "bcast"
        elif name  == "button":      tyname = "button"
        else: tyname = "output"
    
        mod_dict_outputs[name] = os
        mod_dict_types[name] = tyname
    
    for modname in mod_dict_outputs.keys():
        mod_dict_inputs[modname] = []
    
    for k,v in mod_dict_outputs.items():
        for omod in v:
            mod_dict_inputs[omod] += [k]
    
    mod_names = mod_dict_types.keys()
    
    modules = {}
    for mod_name in mod_names:
        ty   = mod_dict_types[mod_name]
        ins  = mod_dict_inputs[mod_name]
        outs = mod_dict_outputs[mod_name]
    
        if    ty == "flip-flop":
            m = Flip_flop(mod_name, ins, outs)
        elif  ty == "con":
            m = Con(mod_name, ins, outs)
        elif  ty == "bcast":
            m = Bcaster(mod_name, ins, outs)
        elif  ty == "button":
            m = Button(mod_name, ins, outs)
        elif  ty == "output":
            m = Output(mod_name, ins, outs)
        else:
            assert False
        modules[mod_name] = m

    return modules

def add_pulses(pulse_q: Queue, new_pulses: list[tuple[int,str]])->Queue:
    for p in new_pulses:
        pulse_q.put(p)
    return pulse_q

def get_pulses(ms: dict[Module]) -> tuple[int,int]:
    pq = Queue()
    
    b = ms["button"]
    nps = b.press()
    pq = add_pulses(pq, nps)
    
    lo_per_press = 0
    hi_per_press = 0
    while not pq.empty():
        pulse, to, fm = pq.get()
        #if pulse == 0 and to == "output":
        #    print(f"{fm:11s} |{pulse}| -> {to}")
        #    assert False
        if pulse == 0:
            lo_per_press += 1
        else:
            hi_per_press += 1
    
        nps = ms[to].handle_pulse(pulse, fm)
        pq = add_pulses(pq, nps)

    return (ms, lo_per_press, hi_per_press)
    
    