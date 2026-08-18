from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User
from app.schemas.agent import (
    AgentCreate,
    AgentResponse,
    AgentUpdate,
)
from app.services.dependencies import (
    get_agent_service,
    get_current_user,
)
from app.services.agent import AgentService

router = APIRouter(
    prefix="/agents",
    tags=["Agents"],
)


@router.post(
    "/",
    response_model=AgentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_agent(
    agent: AgentCreate,
    current_user: User = Depends(get_current_user),
    service: AgentService = Depends(get_agent_service),
):
    return service.create(
        agent=agent,
        owner_id=current_user.id,
    )


@router.get(
    "/",
    response_model=list[AgentResponse],
)
def get_agents(
    service: AgentService = Depends(get_agent_service),
):
    return service.get_all()


@router.get(
    "/{agent_id}",
    response_model=AgentResponse,
)
def get_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service),
):
    try:
        return service.get_by_id(agent_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.put(
    "/{agent_id}",
    response_model=AgentResponse,
)
def update_agent(
    agent_id: int,
    agent: AgentUpdate,
    service: AgentService = Depends(get_agent_service),
):
    try:
        return service.update(
            agent_id=agent_id,
            agent_data=agent,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )


@router.delete(
    "/{agent_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_agent(
    agent_id: int,
    service: AgentService = Depends(get_agent_service),
):
    try:
        service.delete(agent_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )