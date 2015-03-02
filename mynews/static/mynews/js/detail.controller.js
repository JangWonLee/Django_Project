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
		
		/* INIT DETAIL VIEW */
		vm.initDetailView = function(news_id) {
			$http.post('/mynews/' + news_id + '/').success(function(data) {
				vm.news = data.news;
				vm.comment_list = data.comment_list;
				vm.comment_list_count = data.comment_list_count;
			});
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
				vm.comment_list.push(vm.postData);
				vm.commentData = {};
			});
		};
		
		
		/* DELETE COMMENT */
		vm.deleteComment = function(news_id, comment_id) {
			var data = {
					news_id : news_id,
					comment_id : comment_id
			};
			$http.post('/mynews/comment_delete/', data).success(function(data) {
				for(var i = vm.comment_list.length -1; i>=0; i--) {
					if(vm.comment_list[i].comment_id == data.comment_id) {
						vm.comment_list.splice(i, 1);
					}
				}
			});
		};
		
		
		/* EDIT COMMENT */
		vm.editCommentText = null;
		vm.editComment = function(comment_id) {
			for(var i = vm.comment_list.length -1; i>=0; i--) {
				if(vm.comment_list[i].comment_id == comment_id) {
					vm.editCommentText = vm.comment_list[i].comment_text;
				}
			}
			vm.selectedComment = comment_id;
		};
		
		
		/* CANCEL COMMENT */
		vm.cancelComment = function() {
			vm.editCommentText = null;
			vm.selectedComment = null;
		};

		
		/* SUBMIT COMMENT */
		vm.submitComment = function(news_id, comment_id) {
			var data = {
					news_id : news_id,
					comment_id : comment_id,
					edit_text : vm.editCommentText
			};
			$http.post('/mynews/comment_edit/', data).success(function(data) {
				for(var i = vm.comment_list.length -1; i>=0; i--) {
					if(vm.comment_list[i].comment_id == comment_id) {
						vm.comment_list[i].comment_text = vm.editCommentText;
					}
				}
				vm.editCommentText = null;
				vm.selectedComment = null;
			});
		};
	}

})();