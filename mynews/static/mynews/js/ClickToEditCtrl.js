//function ClickToEditCtrl($scope) {
//	$scope.title = "test example";
//	$scope.editorEnabled = false;
//	
//	$scope.enableEditor = function() {
//		$scope.editorEnabled = true;
//		$scope.editableTitle = $scope.title;
//	};
//	
//	$scope.disableEditor = function() {
//		$scope.editorEnabled = false;
//	};
//	
//	$scope.save = function() {
//		$scope.title = $scope.editableTitle;
//		$scope.disableEditor();
//	};
//}

function ClickToEditCtrl() {
	var vm = this;
	vm.title = "test example";
	vm.editorEnabled = false;
	
	vm.enableEditor = function() {
		vm.editorEnabled = true;
		vm.editableTitle = vm.title;
	};
	
	vm.disableEditor = function() {
		vm.editorEnabled = false;
	};
	
	vm.save = function() {
		vm.title = vm.editableTitle;
		vm.disableEditor();
	};
}