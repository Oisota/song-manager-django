const App = window.App || {};

((App) => {

	function hideModal(selector) {
		const modal = bootstrap.Modal.getInstance(selector);
		modal.hide();
	}

	App.addSongSuccess = () => {
		hideModal('#add-modal');
		const form = document.querySelector('#add-song-form')
		form.reset();
	}
	App.editSongSuccess = () => {
		hideModal('#edit-modal');
	}
	App.deleteSongSuccess = () => {
		hideModal('#delete-modal');
	}

})(App);