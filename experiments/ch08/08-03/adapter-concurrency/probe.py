class AdapterProbe:
 def adapter_state(self):
  manager=self.model_runner.lora_manager
  return dict(registered=sorted(manager.list_adapters()),gpu_slot_ids=list(manager._adapter_manager.lora_index_to_id))
