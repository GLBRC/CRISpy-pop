/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "/packs/";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./app/webpacker/packs/gene_submission.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./app/webpacker/packs/gene_submission.js":
/*!************************************************!*\
  !*** ./app/webpacker/packs/gene_submission.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

throw new Error("Module build failed (from ./node_modules/babel-loader/lib/index.js):\nSyntaxError: /Users/michaelgraham/apps/crispy_public/app/webpacker/packs/gene_submission.js: Unexpected token, expected \",\" (45:36)\n\n  43 |   var children = $('#igv-search-container').children()\n  44 |   var str = $( \"input\" ).first();\n> 45 |   console.log(children.first().val();\n     |                                     ^\n  46 |   //igv.browser.search(locusString);\n  47 |   $(\"html, body\").animate({ scrollTop: 0 }, \"medium\");\n  48 | }\n    at Object.raise (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:6400:17)\n    at Object.unexpected (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:7728:16)\n    at Object.expect (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:7714:28)\n    at Object.parseCallExpressionArguments (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8705:14)\n    at Object.parseSubscript (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8613:29)\n    at Object.parseSubscripts (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8528:19)\n    at Object.parseExprSubscripts (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8517:17)\n    at Object.parseMaybeUnary (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8487:21)\n    at Object.parseExprOps (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8353:23)\n    at Object.parseMaybeConditional (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8326:23)\n    at Object.parseMaybeAssign (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8273:21)\n    at Object.parseExpression (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:8221:23)\n    at Object.parseStatementContent (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10061:23)\n    at Object.parseStatement (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:9932:17)\n    at Object.parseBlockOrModuleBlockBody (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10508:25)\n    at Object.parseBlockBody (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10495:10)\n    at Object.parseBlock (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10479:10)\n    at Object.parseFunctionBody (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:9523:24)\n    at Object.parseFunctionBodyAndFinish (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:9493:10)\n    at /Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10638:12\n    at Object.withTopicForbiddingContext (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:9805:14)\n    at Object.parseFunction (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10637:10)\n    at Object.parseFunctionStatement (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10280:17)\n    at Object.parseStatementContent (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:9970:21)\n    at Object.parseStatement (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:9932:17)\n    at Object.parseBlockOrModuleBlockBody (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10508:25)\n    at Object.parseBlockBody (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:10495:10)\n    at Object.parseTopLevel (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:9861:10)\n    at Object.parse (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:11373:17)\n    at parse (/Users/michaelgraham/apps/crispy_public/node_modules/@babel/parser/lib/index.js:11409:38)");

/***/ })

/******/ });
//# sourceMappingURL=gene_submission-858ddd80df1e3b56b0d1.js.map