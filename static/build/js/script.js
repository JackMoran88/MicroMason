var e,t;$(document).ready(function(){$(".dropdown__content").hide(),$(".dropdown__btn").click(function(){$(this).siblings(".dropdown__content").slideToggle(),$(this).children(".fa").toggleClass(["fa-caret-right","fa-caret-down"])})}),$(document).ready(function(){new ResizeSensor($("nav.navbar"),function(){var e=$(window);$("div.page").css({"padding-top":$("nav.navbar").outerHeight()}),$("section.categories").css({"padding-top":$("nav.navbar").outerHeight()}),console.log("resized"),$(".card__image").height(1.1*$(".card__image").width()),e.width()<=992&&$(".navbar-toggler").is(":visible")?$("div.navbar-collapse").css({"padding-top":$("nav.navbar").outerHeight()}):$("div.navbar-collapse").css({"padding-top":0})}),$(window).scroll(function(){100<$(this).scrollTop()&&$(".js-userline").addClass("hide"),$(this).scrollTop()<80&&$(".js-userline").removeClass("hide")})}),$(document).ready(function(){$("#btn_burger").bind("click",function(){$(this).toggleClass("active"),$(".categories__list_sub").removeClass("active"),$(".categories__list").removeClass("active"),$("#categories").toggleClass("active")}),$("#categories").bind("click",function(){$("#btn_burger").removeClass("active"),$("#categories").removeClass("active")}),$(document).on("keydown",function(e){"Escape"==e.key&&($("#btn_burger").removeClass("active"),$("#categories").removeClass("active"),$("#js-input-search").blur(),$("#js-input-search").val("")),65<=e.keyCode&&e.keyCode<=90&&!$("input").is(":focus")&&($("#js-input-search").is(":focus")||$("#js-input-search").focus().select())}),$(".categories__content .categories__list  li").hover(function(){var e;$(".categories__list_sub").removeClass("active"),$(".categories__list").addClass("active"),$(".categories__list_sub").eq((e=this,Array.from(e.parentNode.children).indexOf(e))).addClass("active")}),$(document).ready(function(){$(document).on("keydown",function(e){})})}),$(document).ready(function(){$("#js-custom-toggler").on("click",function(){$(".animated-burger").toggleClass("open")})}),e="undefined"!=typeof window?window:this,t=function(){if("undefined"==typeof window)return null;var t="undefined"!=typeof window&&window.Math==Math?window:"undefined"!=typeof self&&self.Math==Math?self:Function("return this")(),z=t.requestAnimationFrame||t.mozRequestAnimationFrame||t.webkitRequestAnimationFrame||function(e){return t.setTimeout(e,20)},o=t.cancelAnimationFrame||t.mozCancelAnimationFrame||t.webkitCancelAnimationFrame||function(e){t.clearTimeout(e)};function s(e,t){var n=Object.prototype.toString.call(e),i="[object Array]"===n||"[object NodeList]"===n||"[object HTMLCollection]"===n||"[object Object]"===n||"undefined"!=typeof jQuery&&e instanceof jQuery||"undefined"!=typeof Elements&&e instanceof Elements,o=0,s=e.length;if(i)for(;o<s;o++)t(e[o]);else t(e)}function C(e){if(!e.getBoundingClientRect)return{width:e.offsetWidth,height:e.offsetHeight};var t=e.getBoundingClientRect();return{width:Math.round(t.width),height:Math.round(t.height)}}function _(t,n){Object.keys(n).forEach(function(e){t.style[e]=n[e]})}var n,r=function(t,n){var w=0;function y(){var n,i,o=[];this.add=function(e){o.push(e)},this.call=function(e){for(n=0,i=o.length;n<i;n++)o[n].call(this,e)},this.remove=function(e){var t=[];for(n=0,i=o.length;n<i;n++)o[n]!==e&&t.push(o[n]);o=t},this.length=function(){return o.length}}function i(n,e){var t,i,o,s,r,a,c,d,l,u,f,h,p,v,g,m,$,b;n&&(n.resizedAttached?n.resizedAttached.add(e):(n.resizedAttached=new y,n.resizedAttached.add(e),n.resizeSensor=document.createElement("div"),n.resizeSensor.dir="ltr",n.resizeSensor.className="resize-sensor",t={pointerEvents:"none",position:"absolute",left:"0px",top:"0px",right:"0px",bottom:"0px",overflow:"hidden",zIndex:"-1",visibility:"hidden",maxWidth:"100%"},i={position:"absolute",left:"0px",top:"0px",transition:"0s"},_(n.resizeSensor,t),(o=document.createElement("div")).className="resize-sensor-expand",_(o,t),_(s=document.createElement("div"),i),o.appendChild(s),(r=document.createElement("div")).className="resize-sensor-shrink",_(r,t),_(a=document.createElement("div"),i),_(a,{width:"200%",height:"200%"}),r.appendChild(a),n.resizeSensor.appendChild(o),n.resizeSensor.appendChild(r),n.appendChild(n.resizeSensor),"absolute"!==(d=(c=window.getComputedStyle(n))?c.getPropertyValue("position"):null)&&"relative"!==d&&"fixed"!==d&&"sticky"!==d&&(n.style.position="relative"),l=!1,u=0,f=C(n),v=!(p=h=0),w=0,g=function(){if(v){if(0===n.offsetWidth&&0===n.offsetHeight)return void(w=w||z(function(){w=0,g()}));v=!1}var e,t;e=n.offsetWidth,t=n.offsetHeight,s.style.width=e+10+"px",s.style.height=t+10+"px",o.scrollLeft=e+10,o.scrollTop=t+10,r.scrollLeft=e+10,r.scrollTop=t+10},n.resizeSensor.resetSensor=g,m=function(){u=0,l&&(h=f.width,p=f.height,n.resizedAttached&&n.resizedAttached.call(f))},(b=function(e,t,n){e.attachEvent?e.attachEvent("on"+t,n):e.addEventListener(t,n)})(o,"scroll",$=function(){f=C(n),(l=f.width!==h||f.height!==p)&&!u&&(u=z(m)),g()}),b(r,"scroll",$),w=z(function(){w=0,g()})))}s(t,function(e){i(e,n)}),this.detach=function(e){w&&(o(w),w=0),r.detach(t,e)},this.reset=function(){t.resizeSensor.resetSensor&&t.resizeSensor.resetSensor()}};return r.reset=function(t){s(t,function(e){t.resizeSensor.resetSensor&&e.resizeSensor.resetSensor()})},r.detach=function(e,t){s(e,function(e){e&&(e.resizedAttached&&"function"==typeof t&&(e.resizedAttached.remove(t),e.resizedAttached.length())||e.resizeSensor&&(e.contains(e.resizeSensor)&&e.removeChild(e.resizeSensor),delete e.resizeSensor,delete e.resizedAttached))})},"undefined"!=typeof MutationObserver&&(n=new MutationObserver(function(e){for(var t in e)if(e.hasOwnProperty(t))for(var n=e[t].addedNodes,i=0;i<n.length;i++)n[i].resizeSensor&&r.reset(n[i])}),document.addEventListener("DOMContentLoaded",function(e){n.observe(document.body,{childList:!0,subtree:!0})})),r},"function"==typeof define&&define.amd?define(t):"object"==typeof exports?module.exports=t():e.ResizeSensor=t();