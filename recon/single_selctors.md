One way radio button: 
<div class="customComponent" style="margin-left: 4px">
            <input type="radio" name="tripType" value="oneWay" id="flightSearchForm.tripType.oneWay" checked="">
            <label for="flightSearchForm.tripType.oneWay">
                <span class="control"></span>
                <span class="hidden-accessible">Search flights one way</span>
                <span aria-hidden="true">One way</span>
            </label>
        </div>

Redeem miles checkbox:
<div class="customComponent">
            <input type="checkbox" name="redeemMiles" value="true" id="flightSearchForm.tripType.redeemMiles" checked="checked">
            <label for="flightSearchForm.tripType.redeemMiles">
                <span class="control"></span>
                Redeem miles
            </label>
        </div>

From Input:
<input type="text" name="originAirport" value="LAX" id="reservationFlightSearchForm.originAirport" class="aaAutoComplete ui-autocomplete-input" placeholder="City or airport" autocomplete="off" autocorrect="off">

To Input:
<input type="text" name="destinationAirport" value="JFK" id="reservationFlightSearchForm.destinationAirport" class="aaAutoComplete ui-autocomplete-input" placeholder="City or airport" autocomplete="off" autocorrect="off">

Depart date picker:
<input class="aaDatePicker hasDatepicker" id="aa-leavingOn" name="departDate" type="text" value="11/15/2025" placeholder="mm/dd/yyyy" autocomplete="off">

Search button:
<input type="submit" value="Search" id="flightSearchForm.button.reSubmit" class="btn btn-fullWidth">

<div _ngcontent-wdx-c103="" class="cell large-4 pad-left-sm"><div _ngcontent-wdx-c103="" class="duration">5h 25m</div><div _ngcontent-wdx-c103="" class="stops"><app-stops-tooltip _ngcontent-wdx-c103="" _nghost-wdx-c22=""><span _ngcontent-wdx-c22="" class="nonstop">Nonstop</span><!----><!----></app-stops-tooltip></div></div>

Departure Time:
<div _ngcontent-wdx-c103="" class="flt-times">6:05 AM</div>

Arrival Time:
<div _ngcontent-wdx-c103="" class="flt-times"> 2:30 PM <!----></div>

Flight card:
<button _ngcontent-wdx-c98="" class="btn-flight" id="flight0-product0"><span _ngcontent-wdx-c98="" class="hidden-accessible hidden-product-type">Main</span><div _ngcontent-wdx-c98="" class="premium"></div><!----><div _ngcontent-wdx-c98="" class="trip-type regular">One way</div><app-choose-flights-price-desktop _ngcontent-wdx-c98="" _nghost-wdx-c97=""><span _ngcontent-wdx-c97="" class="per-pax-amount">17.5K</span><!----><div _ngcontent-wdx-c97="" class="per-pax-addon">+ $5.60</div><!----><!----><span _ngcontent-wdx-c97="" class="hidden-accessible hidden-flight-details">One way Main 17.5K + $5.60 for LAX to JFK, departing at 6:05 AM Nonstop</span><!----></app-choose-flights-price-desktop><!----><!----><!----></button>