class GeoObject
  attr_reader :f_id, :area, :perimeter, :id, :land, :name, :status, :rb, :type, :date, :layer, :path, :gen, :kreis_kenn, :z_kreis_ke, :kreis_id, :rs, :two_kreis_ke,:state, :landkey_pa, :rb_codes_r, :longitude, :latitude

  attr_accessor :start_date, :end_date, :date_ranges

  def initialize(args = {})
    @f_id = args[:f_id]
    @area = args[:area]
    @perimeter = args[:perimeter]
    @id = args[:id]
    @land = args[:land]
    @name = args[:name]
    @status = args[:status]
    @rb = args[:rb]
    @type = args[:type]
    @date = args[:date]
    @layer = args[:layer]
    @path = args[:path]
    @gen = args[:gen]
    @kreis_kenn = args[:kreis_kenn]
    @z_kreis_ke = args[:z_kreis_ke]
    @kreis_id = args[:kreis_id]
    @rs = args[:rs]
    @two_kreis_ke = args[:two_kreis_ke]
    @state = args[:state]
    @landkey_pa = args[:landkey_pa]
    @rb_codes_r = args[:rb_codes_r]
    @longitude = args[:longitude]
    @latitude = args[:latitude]
    @start_date = nil
    @end_date = nil
    @date_ranges = nil
  end

  def to_csv
    csv_array = []
    self.instance_variables.each do |attribute|
      csv_array.push(self.instance_variable_get(attribute))
    end
    csv_array
  end

end