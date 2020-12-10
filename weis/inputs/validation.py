import os
import jsonmerge
from wisdem.inputs import load_yaml, write_yaml, validate_without_defaults, validate_with_defaults


froot_wisdem           = os.path.dirname(load_yaml.__file__)
fschema_geom_wisdem    = os.path.join(froot_wisdem, 'geometry_schema.yaml')
fschema_model_wisdem   = os.path.join(froot_wisdem, 'modeling_schema.yaml')
fschema_opt_wisdem     = os.path.join(froot_wisdem, 'analysis_schema.yaml')

froot           = os.path.dirname(os.path.realpath(__file__))
fdefaults_geom  = os.path.join(froot, 'geometry_defaults.yaml')
fschema_geom    = os.path.join(froot, 'geometry_schema.yaml')
fschema_model   = os.path.join(froot, 'modeling_schema.yaml')
fschema_opt     = os.path.join(froot, 'analysis_schema.yaml')
#---------------------
def load_default_geometry_yaml():
    return load_yaml(fdefaults_geom)

def get_geometry_schema():
    wisdem_schema = load_yaml(fschema_geom_wisdem)
    weis_schema   = load_yaml(fschema_geom)
    merged_schema = jsonmerge.merge(wisdem_schema, weis_schema)
    return merged_schema

def load_geometry_yaml(finput):
    merged_schema = get_geometry_schema()
    return validate_with_defaults(finput, merged_schema)

def write_geometry_yaml(instance, foutput):
    merged_schema = get_geometry_schema()
    validate_without_defaults(instance, merged_schema)
    sfx_str = '.yaml'
    if foutput[-5:] == sfx_str:
        sfx_str = ''
    write_yaml(instance, foutput+sfx_str)

def get_modeling_schema():
    wisdem_schema = load_yaml(fschema_model_wisdem)
    weis_schema   = load_yaml(fschema_model)
    weis_schema['properties']['WISDEM'] = wisdem_schema
    return weis_schema

def load_modeling_yaml(finput):
    weis_schema = get_modeling_schema()
    return validate_with_defaults(finput, weis_schema)

def write_modeling_yaml(instance, foutput):
    weis_schema = get_modeling_schema()
    validate_without_defaults(instance, weis_schema)
    sfx_str = '.yaml'
    if foutput[-5:] == sfx_str:
        sfx_str = ''
    write_yaml(instance, foutput+sfx_str)

def get_analysis_schema():
    wisdem_schema = load_yaml(fschema_opt_wisdem)
    weis_schema   = load_yaml(fschema_opt)
    merged_schema = jsonmerge.merge(wisdem_schema, weis_schema)
    return merged_schema

def load_analysis_yaml(finput):
    merged_schema = get_analysis_schema()
    return validate_with_defaults(finput, merged_schema)

def write_analysis_yaml(instance, foutput):
    merged_schema = get_analysis_schema()
    validate_without_defaults(instance, merged_schema)
    sfx_str = '.yaml'
    if foutput[-5:] == sfx_str:
        sfx_str = ''
    write_yaml(instance, foutput+sfx_str)
