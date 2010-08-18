-- Function to create the compounds view that we need for the keyword search
BEGIN;
CREATE VIEW mambomsapp_compounds_view AS 
SELECT 
	mambomsapp_compound.id,
	mambomsapp_compound.dataset_id,
	mambomsapp_compound.compound_name, 
	mambomsapp_compound.cas_name,
	mambomsapp_compound.cas_regno,
	mambomsapp_compound.molecular_formula,
	mambomsapp_compound.molecular_weight,
	COALESCE(mambomsapp_gcmarecord.instrument_id, mambomsapp_lcmarecord.instrument_id) AS instrument_id, 
	COALESCE(mambomsapp_gcmarecord.metabolite_class_id, mambomsapp_lcmarecord.metabolite_class_id) AS metabolite_class_id, 
	COALESCE(mambomsapp_gcmarecord.retention_time, mambomsapp_lcmarecord.retention_time) AS retention_time,
	COALESCE(mambomsapp_gcmethod.derivitization_agent, mambomsapp_lcmethod.derivitization_agent) AS derivitization_agent,
	COALESCE(mambomsapp_gcmarecord_biological_systems.biologicalsystem_id, mambomsapp_lcmarecord_biological_systems.biologicalsystem_id) AS biological_system_id,
	mambomsapp_lcmarecord.mono_isotopic_mass
FROM mambomsapp_compound 
	LEFT OUTER JOIN 	
	mambomsapp_gcmarecord ON (mambomsapp_compound.id = mambomsapp_gcmarecord.compound_ptr_id)
	LEFT OUTER JOIN
		mambomsapp_gcmethod ON (mambomsapp_gcmarecord.method_id = mambomsapp_gcmethod.id)	 	
	LEFT OUTER JOIN
		mambomsapp_gcmarecord_biological_systems ON (mambomsapp_gcmarecord.compound_ptr_id = mambomsapp_gcmarecord_biological_systems.gcmarecord_id)	
	LEFT OUTER JOIN 
	mambomsapp_lcmarecord ON (mambomsapp_compound.id = mambomsapp_lcmarecord.compound_ptr_id)
	LEFT OUTER JOIN
		mambomsapp_lcmethod ON (mambomsapp_lcmarecord.method_id = mambomsapp_lcmethod.id)
	LEFT OUTER JOIN
		mambomsapp_lcmarecord_biological_systems ON (mambomsapp_lcmarecord.compound_ptr_id = mambomsapp_lcmarecord_biological_systems.lcmarecord_id);
COMMIT;        
	
