class GeoObject:

  # initialize object with all properties from CSV file
  def __init__(self, fid, area, perimeter, id, land, name, status, rb, type, date, layer, path, gen, kreis_kenn, z_kreis_ke, kreis_id, rs, two_kreis_ke,state, landkey_pa, rb_codes_r, longitude, latitude):
    self.fid = fid
    self.area = area
    self.perimeter = perimeter
    self.id = id
    self.land = land
    self.name = name
    self.status = status
    self.rb = rb
    self.type = type
    self.date = date
    self.layer = layer
    self.path = path
    self.gen = gen
    self.kreis_kenn = kreis_kenn
    self.z_kreis_ke = z_kreis_ke
    self.kreis_id = kreis_id
    self.rs = rs
    self.two_kreis_ke = two_kreis_ke
    self.state = state
    self.landkey_pa = landkey_pa
    self.rb_codes_r = rb_codes_r
    self.longitude = longitude
    self.latitude = latitude
    # these we will add later
    self.start_date = None
    self.end_date = None
    self.date_ranges = None

  # instance method to return values of all object properties above
  def to_csv(self):
    return [*self.__dict__.values()]
