__all__ = ['generate_uuid']

import uuid
import random

def generate_uuid(version=4, domain="example.com", name=None):
    """
    Generate a UUID with customizable parameters.
    
    Args:
        version (int): UUID version (1, 3, 4, or 5)
        domain (str): Domain name for namespaced UUIDs (versions 3/5)
        name (str): Custom name for namespaced UUIDs (versions 3/5)
        
    Returns:
        str: UUID string
        
    Raises:
        ValueError: For unsupported UUID versions
    """
    if version == 1:
        return str(uuid.uuid1())
    
    elif version == 3 or version == 5:
        namespace = uuid.NAMESPACE_DNS
        
        if not name:
            prefixes = ['user', 'account', 'id', 'profile', 'entity']
            suffixes = ['', str(uuid.uuid4().fields[0])]
            name = f"{random.choice(prefixes)}-{random.choice(suffixes)}"
        
        full_name = f"{name}@{domain}"
        
        if version == 3:
            return str(uuid.uuid3(namespace, full_name))
        else:
            return str(uuid.uuid5(namespace, full_name))
    
    elif version == 4:
        return str(uuid.uuid4())
    
    else:
        raise ValueError("Unsupported UUID version. Use 1, 3, 4, or 5.")