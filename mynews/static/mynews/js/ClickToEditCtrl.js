function ClickToEditCtrl($scope) {
	$scope.title = "test example";
	$scope.editorEnabled = false;
	
	$scope.enableEditor = function() {
		$scope.editorEnabled = true;
		$scope.editableTitle = $scope.title;
	};
	
	$scope.disableEditor = function() {
		$scope.editorEnabled = false;
	};
	
	$scope.save = function() {
		$scope.title = $scope.editableTitle;
		$scope.disableEditor();
	};
}