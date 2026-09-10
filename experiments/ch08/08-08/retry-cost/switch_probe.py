from probe import KVProbe
class SwitchProbe(KVProbe):
    def observe_query(self):
        assert not hasattr(self,'query_counts')
        self.query_counts={}
        count=0
        for name,m in self.model_runner.model.named_modules():
            if hasattr(m,'query_quant') and m.query_quant is not None:
                original=m.impl.forward
                def wrap(original,name):
                    def forward(layer,query,*args,**kwargs):
                        key=name+':'+str(query.dtype)
                        self.query_counts[key]=self.query_counts.get(key,0)+1
                        return original(layer,query,*args,**kwargs)
                    return forward
                m.impl.forward=wrap(original,name);count+=1
        return count
    def set_query_mode(self,quantized):
        self.query_counts={};count=0
        for m in self.model_runner.model.modules():
            if hasattr(m,'query_quant') and m.query_quant is not None:
                m.impl.supports_quant_query_input=quantized;count+=1
        return count
    def query_observation(self):
        return self.query_counts
