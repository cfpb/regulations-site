/*
	* Konami-JS ~ 
	* :: Now with support for touch events and multiple instances for 
	* :: those situations that call for multiple easter eggs!
	* Code: http://konami-js.googlecode.com/
	* Examples: http://www.snaptortoise.com/konami-js
	* Copyright (c) 2009 George Mandis (georgemandis.com, snaptortoise.com)
	* Version: 1.4.1 (3/1//2013)
	* Licensed under the GNU General Public License v3
	* http://www.gnu.org/copyleft/gpl.html
	* Tested in: Safari 4+, Google Chrome 4+, Firefox 3+, IE7+, Mobile Safari 2.2.1 and Dolphin Browser
*/

var Konami=function(e){var t={addEvent:function(e,t,n,r){e.addEventListener?e.addEventListener(t,n,!1):e.attachEvent&&(e["e"+t+n]=n,e[t+n]=function(){e["e"+t+n](window.event,r)},e.attachEvent("on"+t,e[t+n]))},input:"",pattern:"3838404037393739666513",load:function(e){this.addEvent(document,"keydown",function(n,r){r&&(t=r),t.input+=n?n.keyCode:event.keyCode,t.input.length>t.pattern.length&&(t.input=t.input.substr(t.input.length-t.pattern.length));if(t.input==t.pattern){t.code(e),t.input="";return}},this),this.iphone.load(e)},code:function(e){window.location=e},iphone:{start_x:0,start_y:0,stop_x:0,stop_y:0,tap:!1,capture:!1,orig_keys:"",keys:["UP","UP","DOWN","DOWN","LEFT","RIGHT","LEFT","RIGHT","TAP","TAP","TAP"],code:function(e){t.code(e)},load:function(e){this.orig_keys=this.keys,t.addEvent(document,"touchmove",function(e){if(e.touches.length==1&&t.iphone.capture==1){var n=e.touches[0];t.iphone.stop_x=n.pageX,t.iphone.stop_y=n.pageY,t.iphone.tap=!1,t.iphone.capture=!1,t.iphone.check_direction()}}),t.addEvent(document,"touchend",function(n){t.iphone.tap==1&&t.iphone.check_direction(e)},!1),t.addEvent(document,"touchstart",function(e){t.iphone.start_x=e.changedTouches[0].pageX,t.iphone.start_y=e.changedTouches[0].pageY,t.iphone.tap=!0,t.iphone.capture=!0})},check_direction:function(e){x_magnitude=Math.abs(this.start_x-this.stop_x),y_magnitude=Math.abs(this.start_y-this.stop_y),x=this.start_x-this.stop_x<0?"RIGHT":"LEFT",y=this.start_y-this.stop_y<0?"DOWN":"UP",result=x_magnitude>y_magnitude?x:y,result=this.tap==1?"TAP":result,result==this.keys[0]&&(this.keys=this.keys.slice(1,this.keys.length)),this.keys.length==0&&(this.keys=this.orig_keys,this.code(e))}}};return typeof e=="string"&&t.load(e),typeof e=="function"&&(t.code=e,t.load()),t};