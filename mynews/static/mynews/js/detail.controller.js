(function() {
	'use strict';

	angular
		.module('app')
		.controller('DetailController', DetailController)
		.config(function($interpolateProvider) {
			 $interpolateProvider.startSymbol('{$');
			 $interpolateProvider.endSymbol('$}');
		});

	DetailController.$inject = [ '$http' ];
	/* @ngInject */
	function DetailController($http) {
		var vm = this;
		
		vm.initDetailView = function() {
			$http.post('/mynews/detail')
		};
		
		
		/* PUSHPIN STATE CHECK */
		vm.pushpinState = 0;

		vm.isSetPushpinState = function(state) {
			return vm.pushpinState === state;
		};

		vm.setPushpinState = function(state, news_id) {
			var data = {
					news_id : news_id
			};
			
			if (state == 0) {
				$http.post('/mynews/news_clip/', data).success(function() {
					vm.pushpinState = 1;
				});

			} else {
				$http.post('/mynews/news_clip_cancel/', data).success(function() {
					vm.pushpinState = 0;
				});
			}
		};
		
		/* POST COMMENT */
		vm.commentData = {};
		vm.postData = {};
		vm.postDataArray = [];
		
		vm.postComment = function(news_id) {
			vm.commentData.news_id = news_id;
			
			$http.post('/mynews/comment_post/', vm.commentData).success(function(data) {
				vm.postData = data;
				vm.postDataArray.push(vm.postData);
				vm.commentData = {};
			});
		};
		
		/* COMMENT EDIT STATE BUTTON CHECK*/
		vm.commentEditState = 0;
		vm.isSetCommentEditState = function(state) {
			return vm.commentEditState === state;
		};
		vm.setCommentEditState = function(state) {
			if (state === 0) {
				vm.commentEditState = 1;
				
			} else {
				vm.commentEditState = 0;
			}
		};
		
		/* DELETE COMMENT */
		vm.deleteComment = function(news_id, comment_id) {
			console.log("deleteComment call");
			var data = {
					news_id : news_id,
					comment_id : comment_id
			};
			$http.post('/mynews/comment_delete/', data).success(function(data) {
				for(var i = vm.postDataArray.length -1; i>=0; i--) {
					if(vm.postDataArray[i].comment_id == data.comment_id) {
						vm.postDataArray.splice(i, 1);
					}
				}
				console.log("commentDelete success");
			});
		};
		
		/* EDIT COMMENT */
		vm.editComment = function(news_id, comment_id) {
			console.log("editComment call");
			var data = {
					news_id : news_id,
					comment_id : comment_id
			};
			$http.post('/mynews/comment_edit/', data).success(function(data) {
				
				console.log("commentEdit success");
			});
		};
		
	}

})();