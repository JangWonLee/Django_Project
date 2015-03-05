(function() {
	'use strict';
	
	angular
		.module('app')
		.controller('ActivityController', ActivityController)
		.config(function($interpolateProvider) {
			 $interpolateProvider.startSymbol('{$');
			 $interpolateProvider.endSymbol('$}');
		})
		.filter('offset', function() {
			return function(input, start) {
				start = parseInt(start, 10);
				return input.slice(start);
			};
		});
	
	ActivityController.$inject = [ '$http' ];
	/* @ngInject */
	function ActivityController($http) {
		var vm = this;
		
		/* INIT ACTIVITY VIEW */
		vm.initActivityView = function() {
			$http.post('/mynews/activity/').success(function(data) {
				vm.activityList = data.activity_list;
				console.log(vm.activityList.length);
				vm.items = vm.activityList;
				
				var temp = 30;
				console.log("parseint", parseInt(temp,10));
			});
		};
		
		/* PAGINATION */
		vm.activityListPerPage = 10;
		vm.currentPage = 0;
		vm.activityList = [];
		
		vm.range = function() {
			var rangeSize = 5;
			var ret = [];
			var start;
			
//			start = vm.currentPage;
			start = parseInt(vm.currentPage/rangeSize)*rangeSize;
			if(start > vm.pageCount() - rangeSize) {
				start = vm.pageCount() - rangeSize + 1;
			}
			
			for (var i = start; i < start+rangeSize; i++) {
				ret.push(i);
			}
			return ret;
		};
		
		vm.pageCount = function() {
//			console.log("pageCount", Math.ceil(vm.activityList.length / vm.activityListPerPage) - 1);
			return Math.ceil(vm.activityList.length / vm.activityListPerPage) - 1;
		};
		
		vm.prevPage = function() {
			if(vm.currentPage > 0) {
				vm.currentPage--;
			}
		};
		
		vm.prevPageDisabled = function() {
			return vm.currentPage === 0 ? "disabled" : "";
		};
		
		vm.nextPage = function() {
			if(vm.currentPage < vm.pageCount()) {
				vm.currentPage++;
			}
		};
		
		vm.nextPageDisabled = function() {
			return vm.currentPage === vm.pageCount() ? "disabled" : "";
		};
		
		vm.setPage = function(n) {
			vm.currentPage = n;
		};
		
	}
	
})();