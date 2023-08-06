# space_objects_geos

- ![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

- ![coverage](coverage-badge.svg)

```bash
pip install space-objects-geos
```

This is an extension for [space_objects](https://github.com/larrieu-olivier/space_objects) package.

Provides outputs objects for easily work with shapely geometries from the originals outputs objects.

Usefull for geometries calculations and geojson representation for web display.

### sample

```python
from space_objects.models import SatelliteActive
from space_objects_geos.outputs import OrbitObjectGeos, PositionObjectGeos

your_position = {
    "observation_position_longitude": 1.433333,
    "observation_position_latitude": 43.6,
}

satellite_name = "ISS (ZARYA)"
iss_object = SatelliteActive(satellite_name, **your_position)

position = PositionObjectGeos(iss_object.get_position())
orbit = OrbitObjectGeos(iss_object.get_orbit())

print(position.geojson)
print(orbit.geojson)
```

position geojson

![position geojson](assets/images/position_geojson.png)

orbit geojson

![orbit geojson](assets/images/orbit_geojson.png)
