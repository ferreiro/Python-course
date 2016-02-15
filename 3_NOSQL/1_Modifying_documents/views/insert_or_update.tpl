% include('header.tpl')

<h1>
	Insert if not exist<br /> or update in other case
</h1>

<form action="/insert_or_update" method="POST">


	<fieldset class="input">
		<label for="_id">
			Name
		</label>
		<input name="_id" type="text" placeholder="Your username" />
	</fieldset>

	<fieldset class="input">
		<label for="country">
			Country
		</label>
		<input name="country" type="text" placeholder="Country" />
	</fieldset>

	<fieldset class="input">
		<label for="zip">
			Country
		</label>
		<input name="zip" type="text" placeholder="Zip" />
	</fieldset>

	<fieldset class="input">
		<label for="email">
			Email
		</label>
		<input name="email" type="text" placeholder="Email" />
	</fieldset>

	<fieldset class="input">
		<label for="gender">
			Gender
		</label>
		<input name="gender" type="text" placeholder="Gender" />
	</fieldset>

	<fieldset class="input">
		<label for="likes">
			Likes
		</label>
		<input name="likes" type="text" placeholder="Likes" />
	</fieldset>

	<fieldset class="input">
		<label for="password">
			Password
		</label>
		<input name="password" type="text" placeholder="Password" />
	</fieldset>

	<fieldset class="input">
		<label for="year">
			Year
		</label>
		<input name="year" type="text" placeholder="Year" />
	</fieldset>

	<fieldset class="button">
		<input type="submit" value="Send me!">
	</fieldset>

</form>

% include('footer.tpl')