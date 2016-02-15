	
	% include('header.tpl')

	<h1 class="title">Results for your query:</h1>
	
	% if len(userList) <= 0:

		<h2 class="subtitle">
			No users found with that parameters values
		</h2> 
	% else:

		<h2 class="subtitle">
			<strong>{{totalResults}}</strong> results
		</h2>

		<table style="width:100%">
			<tbody>

				<tr>
					<th><p>ID</p></th>
					<th><p>Email</p></th> 
					<th><p>Password Hash</p></th>
					<th><p>Gender</p></th>
					<th><p>Country</p></th>
					<th><p>Zip</p></th>
					<th><p>Year</p></th>
					<th><p>Likes</p></th>
				</tr>

				% for user in userList:
				<tr>
					<td><p>{{user['_id']}}</p></td>
					<td><p>{{user['email']}}</p></td> 
					<td><p>{{user['password']}}</p></td>
					<td><p>{{user['gender']}}</p></td>
					<td><p>{{user['address']['country']}}</p></td>
					<td><p>{{user['address']['zip']}}</p></td>
					<td><p>{{user['year']}}</p></td>
					<td><p>
						% for like in user['likes']:
						{{like}}
						% end
						</p>
					</td>
				</tr>
				% end
			</tbody>
		</table>

	% end

% include('footer.tpl')