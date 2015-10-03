(function ($) {
	"use strict";
	$.tpl = function (s) {
		var rex = /<%=?(.*?)%>/g, sQuote = '_SQ%SQ_', origCode = s, funcCode, wrappedCode, r;

		s = s.replace(/[\r\n]/g, ""); // in case it's coming from ajax/textarea/cdata
		s = s.replace(rex, function (matcher, group, offset) {
			group = group.replace(/'/g, sQuote); // inside js, never escape single quotes
			return ((matcher.charAt(2) === "=") ? // <%= ... %> vs <% ... %>
				(sQuote + "; " + "__out += " + group + "; " + "__out += " + sQuote) :
				(sQuote + ";\n" + group + "\n" + "__out += " + sQuote));
		});

		funcCode = ("var __out = " + sQuote + s + sQuote + "; return __out;\n")
			.replace(/'/g, "\\'")
			.replace(new RegExp(sQuote, 'g'), "'");

		wrappedCode = "var T=arguments[0]||{};try{with(T){\n" + funcCode +
			"\n}}catch(__e){console.error(__e);console.info(this.code);}";

		r = function (obj) { return r.run(obj); };
		r.run = new Function(wrappedCode);
		r.code = {wrapped: wrappedCode, func: funcCode, original: origCode};
		return r;
	};
}(jQuery));